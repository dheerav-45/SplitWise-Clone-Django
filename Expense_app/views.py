# hzlg gmwe xclc rlvp passkey

from django.shortcuts import render,redirect

from django.views.generic import View,CreateView,ListView,DetailView,UpdateView

from Expense_app.forms import *

from Expense_app.models import *

from django.contrib.auth import authenticate,login,logout

from django.utils.decorators import method_decorator

from django.core.mail import send_mail

from django.urls import reverse_lazy

from django.conf import settings #import into settings

import random

def is_user(fn):

    def wapper(request,**kwargs):

        id =kwargs.get('pk')

        data=ExpenseModels.objects.get(id=id)

        if data.user_id==request.user:

            return fn(request,**kwargs)
        else:
            return redirect('login')
        
    return wapper


def login_required(fn):

    def wapper(request,**kwargs):

        if not request.user.is_authenticated:

            return redirect('login')
        else:

            return fn(request,**kwargs)
        
    return wapper

class BaseView(View):

    def get(self,request):

        return render(request,'base.html')
    
class HomeView(View):

    def get(self,request):

        return render(request,'home.html')

class SigupView(View):

    def get(self,request):

        form  =UserregisterForm

        return render(request,'signup.html',{'form':form})

    def post(self,request):

        form =UserregisterForm(request.POST)

        if form.is_valid():

            User.objects.create_user(**form.cleaned_data)

            subject ='Splitwise Welcome mail'

            message =f"Hii {form.cleaned_data['username']} Welcome to splitwise from now on we can calculate your"

            from_email =settings.EMAIL_HOST_USER
            recipient_list=[form.cleaned_data.get('email')]

            send_mail(subject,message,from_email,recipient_list,fail_silently=True)

            return redirect('login')
        
        form=UserregisterForm

        return render(request,'signup.html',{'form':form})
    
class LoginView(View):

    def get(self,request):

      form =LoginForm

      return render(request,'login.html',{'form':form})
    
    def post(self,request):

        form=LoginForm(request.POST)

        if form.is_valid():

            username=form.cleaned_data.get('username')
    
            password=form.cleaned_data.get('password')

            data=authenticate(request,username=username,password=password)

            if data:
    
                login(request,data)
    
            return redirect('homeview')
            
        form=LoginForm

        return render(request,'login.html',{'form':form})
    

class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect('Home')
    

@method_decorator(decorator=login_required,name='dispatch')
class Add_ExpenseView(View):

    def get(self,request):

        form=ExpenseForm

        return render(request,'Expanse.html',{'form':form})
    
    def post(self,request):

        form=ExpenseForm(request.POST,request.FILES)

        if form.is_valid():

            amount=form.cleaned_data.get('amount')

            users=User.objects.exclude(id=request.user.id)

            print(users)

            split_amount=amount/(len(users)+1)

            expense=ExpenseModels.objects.create(**form.cleaned_data,user_id=request.user)

            for i in users:

                Splitmodel.objects.create(user=i,expense=expense,split_amount=split_amount)

                balance,created=BalanceModel.objects.get_or_create(amount_payer=i,amount_receiver=request.user,defaults={"Balance_amount":split_amount})

                if not created:

                    balance.Balance_amount+=split_amount

                    balance.save()
        return redirect('Add_Expanse')


@method_decorator(decorator=login_required,name='dispatch')
class ExpenseListView(ListView):

    model =ExpenseModels

    template_name="expence_read.html"

    context_object_name="data"

    def get_queryset(self):

        return ExpenseModels.objects.filter(user_id=self.request.user)
    
@method_decorator(decorator=login_required,name='dispatch')
class ExpanseDetails(DetailView):

    model=ExpenseModels

    template_name="expanse_detail.html"

    context_object_name='data'

@method_decorator(decorator=login_required,name='dispatch')
@method_decorator(decorator=is_user,name='dispatch')
class ExpanseDelete(View):

    def get(self,request,**kwargs):

        id =kwargs.get('pk')

        ExpenseModels.objects.get(id=id).delete()

        return redirect('Read_Expanse')

@method_decorator(decorator=login_required,name='dispatch')
@method_decorator(decorator=is_user,name='dispatch')
class ExpanseUpdateView(View):

    def get(self,request,**kwargs):

        data=ExpenseModels.objects.get(id =kwargs.get('pk'))

        form =ExpenseForm(instance=data)

        return render(request,'expense_update.html',{'form':form})
    
    def post(self,request,**kwargs):

        data=ExpenseModels.objects.get(id=kwargs.get('pk'))

        form=ExpenseForm(request.POST,instance=data)

        if form.is_valid():

            form.user=request.user

            form.save()

            amount=form.cleaned_data.get('amount')

         

            data=Splitmodel.objects.filter(expense=kwargs.get('pk'))

            for i in data:

                old_split_amount=i.split_amount

                break

            existing_balance=BalanceModel.objects.filter(amount_receiver=request.user)

            for i in existing_balance:

                for j in data:

                    if i.amount_payer==j.user:

                        i.Balance_amount-=old_split_amount

                        i.save()

            new_split_amount=amount/(data.count()+1)

            for i in data:

                i.split_amount=new_split_amount
                i.save()

            for j in existing_balance:

                if j.amount_payer==i.user:

                    j.Balance_amount+=i.split_amount

                    j.save()

                    break
        
        return redirect('homeview')
    


class Add_settileupView(View):

    def get(self,request):

        form =SettilmentForm

        return render(request,'settile_form.html',{'form':form})
    
    def post(self,request):

        form=SettilmentForm(request.POST)

        if form.is_valid():

            amount_reciever=form.cleaned_data.get('receiver_user')

            amount=form.cleaned_data.get('settle_amount')

            u_name=User.objects.get(username=amount_reciever)

            Settlement.objects.create(**form.cleaned_data,pay_user=request.user)

            data=BalanceModel.objects.get(amount_payer=request.user,amount_receiver=u_name)

            if data:

                if data.Balance_amount >= amount:

                    data.Balance_amount -=amount

                    data.save()

                    if data.Balance_amount == 0:

                        data.delete()
               
        return redirect('homeview')

class SettilementListView(View):

    def get(self,request):

        data=Settlement.objects.filter(pay_user=request.user)

        return render(request,'settilment_list.html',{'data':data})
    

# class SettilementDetails(View):

#     def get(self,request,**kwargs):
        
#         id =kwargs.get('pk')

#         data=Settlement.objects.get(id =id)

#         return render(request,'settilment_detail.html',{'data':data})
    
    
class SettilmentUpdate(View):

    def get(self,request,**kwargs):

        id =kwargs.get('pk')

        data=Settlement.objects.get(id=id)

        form=SettilmentForm(instance=data)

        return render(request,'settilment_Update.html',{'form':form})
    
    def post(self,request,**kwargs):

        id =kwargs.get('pk')

        data=Settlement.objects.get(id=id)

        form=SettilmentForm(request.POST,instance=data)

        if form.is_valid():

            form.save()

        return redirect('Read_Expanse')

class SettilmentDelete(View):

    def get(self,request,**kwargs):

        id =kwargs.get('pk')

        data=Settlement.objects.get(id =id)

        data.delete()

        return redirect('settil_List')
        

class ForgetPasswordView(View):

    def get(self,request):

        form=ForgotForm

        return render(request,'forget.html',{'form':form})
    
    def post(self,request):

        form=ForgotForm(request.POST)

        user=User.objects.get(username=request.POST.get('username'))

        if user:

            otp=random.randint(1000,9999)

            request.session['otp']=otp

            request.session['username']=user.username

            send_mail(subject="password Forget",message=str(otp),from_email=settings.EMAIL_HOST_USER,recipient_list=[user.email])

        return redirect('OTP')
    

class OtpVerify(View):

    def get(self,request):

        form=OtpForm

        return render(request,'otp.html',{'form':form})
    
    def post(self,request):

        new_otp=request.POST.get('otp') 

        if int(new_otp)==request.session.get('otp'):

            return redirect('reset')
        
        return redirect('forgot')
    
class ResetPasswordView(View):

    def get(self,request):

        form=ResetPasswordForm

        return render(request,'resetpwd.html',{'form':form})
    
    def post(self,request):

        password=request.POST.get('password')

        c_password=request.POST.get('conform_password')

        if password==c_password:

            username=request.session.get('username')

            data=User.objects.get(username=username)

            

            data.set_password(c_password)

            data.save()

            return redirect('login')
        
        return redirect('reset')

########################################
import razorpay

class PremiumView(View):

    def get(self,request):

        client =razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

        user =request.user

        data=client.order.create(data={"amount":50000,"currency":"INR"})

        summery=PaymentSummery.objects.create(premium_user=user,order_id=data['id'],amount=data['amount'])

        context={"summery":summery,"razorpay_key_id":settings.RAZORPAY_KEY_ID,"order_id":data['id'],"amount":data['amount']}

        return render(request,"payment.html",context)
    

class PaymentSuccessView(View):

    def post(self,request):

        payment_id=request.POST.get('razorpay_payment_id')

        order_id=request.POST.get('razorpay_order_id')

        data=PaymentSummery.objects.filter(order_id=order_id).first() 
        
        if data:

            data.payment_status=True

            data.payment_id=payment_id

            data.save()

        return redirect('homeview')

class profileView(View):

    def get(self,request):

        form=profileForm(instance=request.user)

        return render(request,'profile.html',{'form':form})
    
class profile_updateView(View):

    def get(self,request):

        form=profileForm(instance=request.user)

        return render(request,'profile_update.html',{'form':form})

    def post(self,request):

        form=profileForm(request.POST,instance=request.user)

        if form.is_valid():

            form.save()
            print('sucess')
            return redirect('profile')
        return render(request,'profile_update.html',{'form':form})
class BlancesView(View):
    
    def get(self,request):
        balances = BalanceModel.objects.filter(
            amount_payer=request.user
        ) | BalanceModel.objects.filter(
            amount_receiver=request.user
        )

        return render(request, 'balance_list.html', {
            'balances': balances,
            'user': request.user
        })
