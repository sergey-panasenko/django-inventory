"""
register inventory model in django administration
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse

from .models import Stock, Image, Item, Box, Tag
from .pdf import code_labels

admin.site.site_header = _('Inventory')

LINK_HTML = '<a href="{}" target="_blank">{}</a>'


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
    list_display = ('__str__', 'box_link', 'tags_list',)
    list_display_links = ['__str__', ]
    search_fields = ['name', ]
    list_filter = ['box__stock', 'tags', 'box']
    autocomplete_fields = ('tags',)
    inlines = [ImageInline]

    def tags_list(self, obj):
        """ list of item tags in item list """
        if obj.tags:
            return ', '.join([tag.name for tag in obj.tags.all()])
        return '-'
    tags_list.short_description = _('tags')

    def box_link(self, obj):
        """ link to item box """
        if not obj.box:
            return '-'
        return format_html(
            LINK_HTML,
            reverse('admin:django_inventory_app_box_change',
                    args=(obj.box.id, )),
            obj.box.__str__())
    box_link.short_description = _('Box')


class ItemInline(admin.TabularInline):
    """ Inline Item for box """
    fields = ['name', ]
    model = Item
    extra = 1


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    """ Register Box Model in Admin """
    list_display = ('__str__', 'front', 'stock', 'items', )
    list_display_links = ['__str__']
    search_fields = ['code']
    list_filter = ['stock', ]
    readonly_fields = ('code', '__str__')
    inlines = [ItemInline]
    actions = ['print_labels']
    fieldsets = (
        (None, {
            'fields': ('__str__',)
        }),
        ('Optional', {
            'classes': ('collapse', ),
            'fields': ('stock', 'description', ),
        }),
    )

    def front(self, obj):
        """ link to front on box list """
        return format_html(
            LINK_HTML,
            reverse('code', args=(obj.__str__(), )), '⮕')

    def items(self, obj):
        """ link to ibem edit or items list """
        items = Item.objects.filter(box=obj)
        if not items.count():
            return '-'
        if items.count() == 1:
            return format_html(
                LINK_HTML,
                reverse('admin:django_inventory_app_item_change',
                        args=(items[0].id, )),
                items[0].__str__())
        url = '{}?box__id__exact={}'.format(
            reverse("admin:django_inventory_app_item_changelist"),
            obj.id)
        return format_html(LINK_HTML, url, "⮕")
    items.short_description = _('Item(s)')

    def save_model(self, request, obj, form, change):
        """ generate code for new box """
        if not obj.code:
            obj.code = obj.generate_code()
        super().save_model(request, obj, form, change)

    def print_labels(modeladmin, request, queryset):
        """ print box labels """
        codes = [box.code for box in queryset]
        return code_labels(codes, request)
    print_labels.short_description = _('Print label(s)')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Register Tag Model in Admin """
    search_fields = ['name']

    def get_ordering(self, request):
        """ ordering tags by name """
        return ['name']
