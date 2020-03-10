from django.contrib import admin

from .models import Item, OrderItem,Order,  Coupon, Refund, Address, UserProfile,Novels,Stationery,\
    Sciences,Languages, Stk, ItemList, ShopApplication, bookshop


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    # 'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        # 'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        # 'country',
        # 'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type']
    search_fields = ['user', 'street_address', 'apartment_address']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'total']
    readonly_fields = ('total',)

admin.site.register(Item)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Stk)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(Novels)
admin.site.register(Stationery)
admin.site.register(Sciences)
admin.site.register(Languages)
admin.site.register(ItemList)
admin.site.register(ShopApplication)
admin.site.register(bookshop)


