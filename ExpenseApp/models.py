from django.db import models
from django.utils.translation import gettext as _ 
from django.utils import timezone
# Create your models here.

class Expense(models.Model):
    
    name = models.CharField(_(""), max_length=100)
    amount = models.DecimalField(_(""), max_digits=10, decimal_places=2)
    category = models.CharField(_(""), max_length=50)
    created_date = models.DateTimeField(_("") ,blank=True, null=True
                                        # , auto_now_add=True
                                        )
    updated_date = models.DateTimeField(_(""), auto_now=True)

    def __str__(self):
        return self.name
