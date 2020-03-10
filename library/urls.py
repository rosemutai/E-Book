from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [

    path('', views.index, name='index'),
    path('books/', views.BookListView, name='books'),
    path('book/<int:pk>', views.BookDetailView, name='book-detail'),
    path('book/create/', views.BookCreate, name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate, name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete, name='book_delete'),

    path('borrowed', views.borrowed_list, name ='borrowed_list'),

    path('member/<int:pk>/delete/', views.MemberDelete, name='member_delete'),
    path('member/create/', views.MemberCreate, name='member_create'),
    path('member<int:pk>/update/', views.MemberUpdate, name='member_update'),
    path('member/<int:pk>', views.MembertDetail, name='member_detail'),
    path('member/', views.MemberList, name='member_list'),
    path('member/book_list', views.member_BookListView, name='book_member'),
    path('book/<int:pk>/request_issue/', views.member_request_issue, name='request_issue'),
    # path('member/<int:pk>/getFine', views.getFine, name='getFine'),

    # path('feed/', LatestEntriesFeed(), name='feed'),
    path('return/<int:pk>', views.ret, name='ret'),
    path('rating/<int:pk>/update/', views.RatingUpdate, name='rating_update'),
    path('rating/<int:pk>/delete/', views.RatingDelete, name='rating_delete'),

    path(r'^search_b/', views.search_book, name="search_b"),
    path(r'^search_m/', views.search_member, name="search_m")
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/register', views.register, name="register"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)