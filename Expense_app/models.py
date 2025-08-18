from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class ExpenseModels(models.Model):

    amount=models.DecimalField(max_digits=10,decimal_places=2)

    created_data=models.DateTimeField(auto_now_add=True)

    description=models.TextField()

    bill_image=models.ImageField(upload_to='bill_images',null=True,blank=True)

    user_id=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount) 

class Splitmodel(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="split_users")

    expense=models.ForeignKey(ExpenseModels,on_delete=models.CASCADE,related_name="split_expenses")

    split_amount=models.DecimalField(max_digits=10,decimal_places=2)

    status=models.BooleanField(default=False)

#pay_user,receieving_user,sttled_amount

class Settlement(models.Model):
    

    pay_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='amount_payer')

    receiver_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='amount_receiver')

    settle_amount=models.DecimalField(max_digits=10,decimal_places=2)

    paid_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return  self.pay_user



class BalanceModel(models.Model):

    amount_payer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='payer')

    amount_receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')

    Balance_amount=models.DecimalField(max_digits=10,decimal_places=2)
    
class PaymentSummery(models.Model):

    premium_user=models.ForeignKey(User,on_delete=models.CASCADE)

    order_id=models.CharField(max_length=100)

    payment_status=models.BooleanField(default=False)

    payment_id=models.CharField(max_length=100,null=True,blank=True)

    amount=models.IntegerField()

    create_date=models.DateField(auto_now_add=True)