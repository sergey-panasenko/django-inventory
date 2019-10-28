'''
Models for inventory
'''
from random import randint
from django.db import models
from django.utils.translation import gettext_lazy as _



class Stock(models.Model):
    ''' Stock model '''
    name = models.CharField(
        verbose_name=_('name'),
        max_length=64,
    )
    description = models.TextField(
        verbose_name=_('description'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('stock')
        verbose_name_plural = _('stocks')


class Box(models.Model):
    ''' Box model '''
    code = models.PositiveIntegerField(
        verbose_name=_('code'),
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        verbose_name=_('stock'),
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_('description'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return hex(self.code)[2:]

    def generate_code(self):
        code = randint(1, 0xFFFFFFF) + 3 * 0x10000000
        while Box.objects.filter(code=code).first():
            code = randint(1, 0x7FFFFFFF)
        return code

    class Meta:
        verbose_name = _('box')
        verbose_name_plural = _('boxes')


class Tag(models.Model):
    """ Model for tags """
    name = models.CharField(max_length=120, verbose_name=_('tag name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')



class Item(models.Model):
    ''' Item model - All thing in the boxes are described as an item. '''
    name = models.CharField(
        verbose_name=_('name'),
        max_length=64,
    )
    box = models.ForeignKey(
        Box,
        on_delete=models.PROTECT,
        verbose_name=_('box'),
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name=_('tags'),
        help_text=_('tags'),
    )
    description = models.TextField(
        verbose_name=_('description'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')


class Image(models.Model):
    ''' Image model '''
    image = models.ImageField(
        upload_to='images',
        verbose_name=_('image'),
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        verbose_name=_('item'),
    )

    def __str__(self):
        return _('image') + '-' + str(self.id)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
