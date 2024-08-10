from django.db import models

# Create your models here.
availability_choices = [
    (True, "موجود"),
    (False, "ناموجود"),
]


class Phone(models.Model):
    brand = models.CharField(max_length=200, verbose_name="نام برند", blank=False, null=False)
    brand_country = models.CharField(max_length=200, verbose_name="کشور برند", blank=False, null=False)
    model = models.CharField(max_length=200, verbose_name="مدل", blank=False, null=False, unique=True)
    price = models.IntegerField(verbose_name="قیمت", default=0, null=False, blank=True)
    color = models.CharField(max_length=200, verbose_name="رنگ", null=False, blank=True, default="Black")
    screen_size = models.FloatField(verbose_name="اندازه صفحه", null=False, blank=True, default=5.0)
    is_available = models.BooleanField(verbose_name="موجودی", choices=availability_choices, default=True, null=False,
                                       blank=True)
    creator_country = models.CharField(max_length=200, verbose_name="کشور سازنده", blank=True, null=False,
                                       default="China")

    def __str__(self):
        return self.model
