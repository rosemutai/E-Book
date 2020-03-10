from django.urls import path
from .views  import CheckoutView, HomeView,OrderSummaryView,ItemDetailView,add_to_cart,remove_from_cart,remove_single_item_from_cart, RequestRefundView
from . import views


app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    # path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),

    path('textbooks', views.textbooks, name="textbooks"),
    path('exercisebooks', views.exercisebooks, name="exercisebooks"),
    path('pens', views.pens, name="pens"),
    path('sports', views.sports, name="sports"),
    path('art', views.art, name="art"),
    path('stationery', views.stationeries, name="stationeries"),
    path('uploadfile', views.upload_file, name="upload_file"),
    path('apply', views.apply, name="apply"),
    path('approveseller', views.approveseller, name="approveseller"),
    path('approvedshops', views.approvedshops, name="approvedshops"),

    path('search', views.search, name='search'),
    path('emailNotification',views.emailNotification,name="emailNotification"),

    path('payitem',views.order_pay,name="payitem"),
    path('stkconfirm/',views.stkconfirm,name="stkconfirm"),
    # path('access/token', views.getAccessToken, name='get_mpesa_access_token')
]
