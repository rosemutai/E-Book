from django.shortcuts import render, redirect
from .models import *
from .forms import  *
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
import re
from django.db.models import Q


# Create your views here.

User = get_user_model()

def logout(request):
    logout(request)
    return redirect('index')


def index(request):
    return  render(request, 'catalog/index.html')

def BookListView(request):
    book_list = Book.objects.all()
    return render(request, 'catalog/book_list.html', locals())

def borrowed_list(request):
    books_borrowed = BorrowedBook.objects.all()
    return render(request,'catalog/result.html', locals())

@login_required
def member_BookListView(request):
    member = Member.objects.get(member_id=request.user)
    bor = Borrower.objects.filter(member=member)
    book_list = []
    for b in bor:
        book_list.append(b.book)
    return render(request, 'catalog/book_list.html', locals())

def BookDetailView(request, pk):
    book = get_object_or_404(Book, id=pk)
    reviews = Reviews.objects.filter(book=book).exclude(review="none")
    try:
        mem = Member.objects.get(member_id=request.user)
        rr = Reviews.objects.get(review="none")
    except:
        pass
    return render(request, 'catalog/book_detail.html', locals())


@login_required
def BookCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())

@login_required
def BookUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Book.objects.get(id=pk)
    form = BookForm(instance=obj)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
def BookDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    return  redirect('index')

  #
  # item = get_object_or_404(Item, slug=slug)
  #   # novel = get_object_or_404(Novels,slug=slug)
  #   # order_novel,created = OrderNovels.objects.get_or_create(
  #   #     novel = novel,
  #   #     user = request.user,
  #   #     ordered = False
  #   # )
  #   order_item, created = OrderItem.objects.get_or_create(
  #       item=item,
  #       user=request.user,
  #       ordered=False
  #   )
@login_required
def member_request_issue(request, pk):
    # obj = Book.objects.get(id=pk)
    obj = get_object_or_404(Book, id=pk )
    book_borrowed = BorrowedBook.objects.get_or_create(
       book = obj,
       user = request.user,

   )
    return render(request, 'catalog/result.html', locals())


    # if m.total_books_due < 2:
    #     message = "book has been issued, You can collect book our library"
    #     a = Borrower()
    #     a.member = m


    #     a.book = obj
    #     a.issue_date = datetime.datetime.now()
    #     obj.available_copies = obj.available_copies - 1
    #     obj.save()
    #     mem.total_books_due = mem.total_books_due + 1
    #     mem.save()
    #     a.save()
    # else:
    #     message = "you have exceeded limit."
    # return render(request, 'catalog/result.html', locals())

@login_required
def MemberCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = MemberForm()
    if request.method == 'POST':
        form = MemberForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            m = form.cleaned_data['member_id']
            form.save()
            u = User.objects.get(username=m)
            m = Member.objects.get(member_id=m)
            u.email = m.email
            u.save()
            return  redirect('index')
    return render(request, 'catalog/form.html', locals())


@login_required
def MemberUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Member.objects.get(id=pk)
    form = MemberForm(instance=obj)
    if request.method == 'POST':
        form = MemberForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('index')
    return render(request, 'catalog/form.html', locals())

@login_required
def MemberDelete(request, pk):
    obj = get_object_or_404(Member, pk=pk)
    obj.delete()
    return redirect('index')

@login_required
def MemberList(request):
    members = Member.objects.all()
    return render(request, 'catalog/member_list.html', locals())

@login_required
def MembertDetail(request, pk):
    member = get_object_or_404(Member, uuid=pk)
    books=Borrower.objects.filter(member=member)
    return render(request, 'catalog/member_detail.html', locals())

@login_required
def ret(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Borrower.objects.get(id=pk)
    book_pk = obj.book.id
    member_pk = obj.member.id
    member = Member.objects.get(id=member_pk)
    member.total_books_due = member.total_books_due - 1
    member.save()
    book = Book.objects.get(id=book_pk)
    rating = Reviews(review="none", book=book,member=member,rating='2.5')
    rating.save()
    book.available_copies = book.available_copies + 1
    book.save()
    obj.delete()
    return redirect('index')

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title', 'summary','author'])
        book_list= Book.objects.filter(entry_query)
    return render(request, 'catalog/book_list.html', locals())

def search_member(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['member_id','first_name','email'])
        members = Member.objects.filter(entry_query)
    return render(request,'catalog/member_list.html',locals())


@login_required
def RatingUpdate(request, pk):
    obj =Reviews.objects.get(id=pk)
    form = RatingForm(instance=obj)
    if request.method == 'POST':
        form = RatingForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('book-detail',pk=obj.book.id)
    return render(request, 'catalog/form.html', locals())

@login_required
def RatingDelete(request, pk):
    obj = get_object_or_404(Reviews, pk=pk)
    memb=Member.objects.get(member_id=request.user)
    if not memb == obj.member:
        return redirect('index')
    pk = obj.book.id
    obj.delete()
    return redirect('book_detail',pk)

