from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Stock, Image, Item, Box, Tag
from .pdf import code_labels

admin.site.site_header = _('Inventory')


class BoxInline(admin.TabularInline):
    """ Inline Box for Stock """
    model = Box
    extra = 1


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """ Register Stock Model in Admin """
    search_fields = ['name']
    inlines = [BoxInline]

    def get_ordering(self, request):
        return ['name']


class ImageInline(admin.TabularInline):
    """ Inline Image for Item """
    model = Image
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """ Register Item Model in Admin """
    list_display = ('__str__', 'box', 'tags_list',)# #image
    list_display_links = ['__str__']
    search_fields = ['name',]
    list_filter = ['box__stock', 'tags', 'box']
    autocomplete_fields = ('tags',)
    inlines = [ImageInline]

    def tags_list(self, obj):
        if obj.tags:
            return ','.join([tag.name for tag in obj.tags.all()])
        return '-'
    tags_list.short_description = _('tags')

class ItemInline(admin.TabularInline):
    """ Inline Item for box """
    model = Item
    extra = 1


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    """ Register Box Model in Admin """
    list_display = ('__str__', 'stock', 'items', )
    list_display_links = ['__str__']
    search_fields = ['code']
    list_filter = ['stock', ]
    readonly_fields = ('code',)
    inlines = [ItemInline]
    actions = ['print_labels']

    def items(self, obj):
        items = Item.objects.filter(box=obj)
        if not items.count():
            return '-'
        if items.count() == 1:
            return items.first()
        return items.count()
        return Item.objects.filter(box=obj).count()
    items.short_description = _('Item(s)')

    def save_model(self, request, obj, form, change):
        if not obj.code:
            obj.code = obj.generate_code()
        super().save_model(request, obj, form, change)

    def print_labels(modeladmin, request, queryset):
        codes = [box.code for box in queryset]
        return code_labels(codes, request)
    print_labels.short_description = _('Print label(s)')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Register Tag Model in Admin """
    search_fields = ['name']

    def get_ordering(self, request):
        return ['name']
