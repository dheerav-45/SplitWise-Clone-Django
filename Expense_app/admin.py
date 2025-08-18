from django.contrib import admin

from .models import *
admin.site.register(ExpenseModels)
admin.site.register(Splitmodel)
admin.site.register(Settlement)
admin.site.register(BalanceModel)
admin.site.register(PaymentSummery)

