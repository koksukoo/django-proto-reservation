from django.contrib import admin
from .models import Client, Product, Reservation, ReservationCalendar, ReservationItem


class ReservationItemInline(admin.TabularInline):
    model = ReservationItem
    fields = ['product', 'price']
    readonly_fields = ['price']
    extra = 0


class ReservationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': [
                'total_price',
                'client',
                'calendar'
            ],
        }),
        ('Date information', {
            'fields': [
                'start_time',
                'end_time'
            ]
        })
    )
    inlines = [ReservationItemInline]
    readonly_fields = ('total_price',)
    list_display = ('start_time', 'end_time', 'client', 'total_price', 'calendar')
    list_filter = ('start_time', 'calendar')
    search_fields = ('client__name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ReservationCalendar, CalendarAdmin)
admin.site.register(Reservation, ReservationAdmin)
