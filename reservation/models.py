from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ReservationCalendar(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    products = models.ManyToManyField(Product)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    calendar = models.ForeignKey(ReservationCalendar, on_delete=models.PROTECT)

    @property
    def total_price(self):
        items = self.items.all()
        item_prices = [item for t in items.values_list('price') for item in t]
        price = sum(item_prices, 0)
        return price

    def clean(self):
        filterArgs = {
            'start_time__lte': self.end_time,
            'end_time__gte': self.start_time,
            'calendar__pk': self.calendar.pk
        }
        count = Reservation.objects.filter(
            **filterArgs).exclude(pk=self.pk).count()
        if count > 0:
            raise ValidationError(_('Trying to double book a reservation!'))

    def save(self, *args, **kwargs):
        self.clean()
        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return self.start_time.strftime("%d.%m.%Y %H:%M") + " / " + self.client.name


class ReservationItem(models.Model):
    price = models.FloatField()
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super(ReservationItem, self).save(*args, **kwargs)
