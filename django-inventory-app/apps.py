from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InventoryConfig(AppConfig):
    name = 'django-inventory-app'
    verbose_name = _("Inventory")
