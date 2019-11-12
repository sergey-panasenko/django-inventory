from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InventoryConfig(AppConfig):
    name = 'django_inventory_app'
    verbose_name = _("Inventory")
