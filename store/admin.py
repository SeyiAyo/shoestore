from django.contrib import admin
from .models import Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'rating', 'review_count', 'created_at')
    list_filter = ('created_at', 'rating')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'stock')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Metrics', {
            'fields': ('rating', 'review_count')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
