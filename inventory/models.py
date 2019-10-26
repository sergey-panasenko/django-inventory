'''
Models for inventory
'''
from django.db import models
from django.utils.translation import gettext_lazy as _


class Image(models.Model):
    """ Image model """
    image = ImageField(upload_to='images', verbose_name=_('image'))

    def __str__(self):
        return _('image') + '-' + str(self.id)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')


class Item(models.Model):
    ''' Item model - All thing in the boxes are described as an item. '''
    name = models.CharField(verbose_name=_('Name'), max_length=64)
    brand = models.CharField(verbose_name=_('Brand'), max_length=32,
                             null=True, blank=True)
    model = models.CharField(verbose_name=_('Model'), max_length=32,
                             null=True, blank=True)
    part_number = models.CharField(verbose_name=_('Part number'),
                                   max_length=32, null=True, blank=True)
    notes = models.TextField(verbose_name=_('Notes'), null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True, verbose_name=_('Image'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')


class Stock(models.Model):
    ''' Stock model '''
    name = models.CharField(verbose_name=_('Name'), max_length=64)
    address = models.TextField(verbose_name=_('Address'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('stock')
        verbose_name_plural = _('stocks')


class Box(models.Model):
    ''' Box model '''
    code = models.CharField(verbose_name=_('Code'), max_length=16)
    stock = models.ForeignKey(Stock, default=1, on_delete=models.PROTECT,
                              verbose_name=_('stock'))
    notes = models.TextField(verbose_name=_('Notes'), null=True, blank=True)
    items = models.ManyToManyField(Item, blank=True, verbose_name=_('item'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('box')
        verbose_name_plural = _('boxes')
