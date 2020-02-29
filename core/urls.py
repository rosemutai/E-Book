from django.urls import path
from . import views
from core.views import (
    ItemDetailView,
    NovelDetailView,
    StationeryDetailview,
    StationeriesView,
    SciencesView,
    LanguagesView,
    CheckoutView,
    HomeView,
    NovelsView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('novels/',NovelsView.as_view(),name='novel'),
    path('stationeries/',StationeriesView.as_view(), name='stationeries'),
    path('sciences/',SciencesView.as_view(), name='science'),
    path('languages/',LanguagesView.as_view(),name='language'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('novel/<slug>/',NovelDetailView.as_view(),name='novel'),
    path('stationery/<slug>/',StationeryDetailview.as_view(), name='stationery'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    # path('access/token', views.getAccessToken, name='get_mpesa_access_token')
]
