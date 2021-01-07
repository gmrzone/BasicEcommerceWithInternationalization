from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class CouponCode(models.Model):
    code = models.CharField(max_length=50, db_index=True)
    user = models.ManyToManyField('auth.user', blank=True, related_name='coupons')
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = "CouponCode"
    def __str__(self):
        return self.code
