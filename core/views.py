from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from requests.auth import HTTPBasicAuth
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from base64 import b64decode, b64encode
from datetime import datetime, timedelta, date
from django.utils import timezone
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Item,OrderItem, Order, Address, Coupon, Refund, UserProfile,Stk, ItemList, ShopApplication
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
import re


import random
import string

@csrf_exempt
def MpesaAccessToken(request):
    """
    Function to generate token from the consumer secret and key
    """
    consumer_key = 'GqetbWYIslmgK5nXdBUxYLQT9vK2glYm'
    consumer_secret = 'HY3n8GKkLeAckqqj'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    auth = json.loads(r.text)
    token = auth['access_token']
    return HttpResponse(token)


@csrf_exempt
def lipa_na_mpesa_online(request,phone,amount):
    """
    Initiate stk push to client. Pass phone number of the client and amount to be billed as parameters.
    Will be called by any the other fucntion that requires to perform a billing and return the data response from safaricom
    """
    phone = phone
    amount = amount

    api_transaction_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    BusinessShortCode = 174379;
    LipaNaMpesaPasskey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919';
    access_token = MpesaAccessToken(request)
    data = None

    get_now = datetime.now()
    payment_time = get_now.strftime("%Y%m%d%H%M%S")
    to_encode = '{}{}{}'.format(
        BusinessShortCode, LipaNaMpesaPasskey, payment_time)
    payment_password = (b64encode(to_encode.encode('ascii'))).decode("utf-8")

    if access_token:
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": BusinessShortCode,
            "Password": payment_password,
              "Timestamp": payment_time,
              "TransactionType": "CustomerPayBillOnline",
              "Amount": amount,
              "PartyA": phone,
              "PartyB": BusinessShortCode,
              "PhoneNumber": phone,
              "CallBackURL": ' https://7c05cde2.ngrok.io.io/stkconfirm/',
              "AccountReference": "ebook",
              "TransactionDesc": 'payment'
        }
        response = requests.post(
            api_transaction_URL, json=request, headers=headers)
        # somedata = response[i]
        # data2 = response[i]
        # Stk.objects.create(field =somedata, field2=data2)
        data = response.text

    else:
        print('access token failed')

    return data


@csrf_exempt
@require_POST
def stkconfirm(request):
    if request.method == "POST":
        mpesa_body =request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)


        get_data = mpesa_payment['Body']['stkCallback']
        get_success_data = get_data['CallbackMetadata']

        if get_data:
            MerchantRequestID = get_data[
                'MerchantRequestID']
            CheckoutRequestID = get_data[
                'CheckoutRequestID']
            ResultCode = get_data['ResultCode']
            ResultDesc = get_data['ResultDesc']

            if get_success_data:
                get_items = get_success_data['Item']
                for i in get_items:
                    if i['Name'] == 'Amount':
                        Amount = i.get('Value')
                    elif i['Name'] == 'MpesaReceiptNumber':
                        MpesaReceiptNumber = i.get('Value')
                    elif i['Name'] == 'PhoneNumber':
                        PhoneNumber = i.get('Value')
                    elif i['Name'] == 'Balance':
                        Balance = i.get('Value')
                    elif i['Name'] == 'TransactionDate':
                        TransactionDate = i.get('Value')
                    else:
                        continue

            else:
                Amount = None
                MpesaReceiptNumber = None
                PhoneNumber = None
                Balance = None
                TransactionDate = None

            stk_response = Stk.objects.create(MerchantRequestID=MerchantRequestID, CheckoutRequestID=CheckoutRequestID, \
                                              ResultCode=ResultCode, ResultDesc=ResultDesc, Amount=Amount,
                                              MpesaReceiptNumber=MpesaReceiptNumber, \
                                              PhoneNumber=PhoneNumber, Balance=Balance, TransactionDate=TransactionDate)

        print(mpesa_payment)


        context = {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context))



def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)




def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


def textbooks(request):
    books = Item.objects.filter(category="TB")
    return  render(request, "textbooks.html", locals())

def exercisebooks(request):
    exbooks = Item.objects.filter(category="EB")
    return  render(request, "exercisebooks.html", locals())

def pens(request):
    pens = Item.objects.filter(category="P")
    return  render(request, "pens.html", locals())

def sports(request):
    sports = Item.objects.filter(category="SP")
    return  render(request, "sports.html", locals())

def art(request):
    arts = Item.objects.filter(category="A")
    return  render(request, "art.html", locals())

def stationeries(request):
    stationeries = Item.objects.filter(category="OS")
    return  render(request, "stationeries.html", locals())




class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    # model = Novels
    template_name = "product.html"



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")


def emailNotification(ref_code):
    order = Order.objects.get(id=ref_code)
    subject = 'EBook order'
    message = 'Dear {},\n\nYou have successfully placed an order.' \
              'On payment collect your order from our office near you\Your order id is {}.'.format(order.user,ref_code)

    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['chepngetichrose2030@gmail.com',]
    mail_sent = send_mail( subject, message, email_from, recipient_list )

    return mail_sent


@csrf_exempt
def order_pay(request):
    if request.method == "POST":
        orderid = request.POST['orderid']
        order=Order.objects.get(id=orderid)
        phone='254'+ str(order.phone)
        amount=1
        mpesa = lipa_na_mpesa_online(request,phone,amount)
        print(mpesa)
        u = User.objects.get(email=request.COOKIES['email'])
        items = OrderItem.objects.filter(user=u, paid=False)
        contents = []

        for item in items:
            content = Item.objects.get(slug=item.slug)
            contents += [content]
            Order.objects.create(order=order, contents=Item.objects.get(slug=item.slug), price=item.price,
                                     quantity=item.quantity)
        total = total(items)
        emailNotification(order.id)
    return render(request, 'payment.html', locals())




def checkpay(request):
    return render(request,'order_snippet.html',{'error':'Payment Received','state':'Payment Success','user':request.COOKIES['email']})



def search(request):
    items = Item.objects.filter(~Q(image=''))

    if request.method == 'POST':
        search = request.POST['search']
        print(search)
        items = Item.objects.filter(~Q(image='') & Q(category__icontains=search))

    user = request.user
    return render(request, 'home.html', {'items': items, 'user': user})


def upload_file(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        file = request.POST['file']

        upload = ItemList.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email,
                                         list_img=file)
        if upload:
            message = 'Successfully uploaded your list.'
        else:
            message = 'There was an error uploading you list.'
        return render(request, 'upload.html', {'message': message})

    message = ''
    return render(request, 'upload.html', {'message': message})


def apply(request):
    message = ''
    if request.method == 'POST':
        shopname = request.POST['shopname']
        description = request.POST['description']

        u = User.objects.get(email=request.COOKIES['email'])

        print(u)
        check_if_shopowner = ShopApplication.objects.filter(user=u,accept=True)
        if not check_if_shopowner:
            application = ShopApplication.objects.create(user=u,shopName=shopname,description=description)
        else:
            application = None

        if application:
            subject = 'EBook order'
            message = 'Your application has been received and we will get back to you.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['chepngetichrose2030@gmail.com', ]
            # fail_silently = False
            mail_sent = send_mail(subject, message, email_from, recipient_list)
            print(mail_sent)
        else:
            pass

    else:
        pass

    return render(request, 'apply.html', {'message': message})

def approveseller(request):
    applications = ShopApplication.objects.filter(accept=False,cancel=False)
    return render(request, 'approveseller.html', {'applications':applications})

def approvedshops(request):
    shops = ShopApplication.objects.filter(accept=True)
    return render(request, 'approvedshops.html', {'shops':shops})
