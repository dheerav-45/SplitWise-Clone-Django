"""
URL configuration for splitwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Expense_app.views import *

def redirect_home(request):

    return redirect('Home')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("",redirect_home),
    path('splitwise',BaseView.as_view(),name='Home'),

    path('Splite_Wise/Signup/',SigupView.as_view(),name='signup'),
    path('Splite_Wise/Login/',LoginView.as_view(),name='login'),
    path('splite_wise/home/',HomeView.as_view(),name='homeview'),
    path('splite_wise/Logout/',LogoutView.as_view(),name='logout'),

    path('Splite_Wise/Add_Expanse/',Add_ExpenseView.as_view(),name='Add_Expanse'),
    path('splite_Wise/Read_Expanse/',ExpenseListView.as_view(),name='Read_Expanse'),
    path('splite_Wise/Detail_Expanse/<int:pk>/',ExpanseDetails.as_view(),name='Detail_Expanse'),
    path('splite_Wise/Delete_Expanse/<int:pk>/',ExpanseDelete.as_view(),name='Delete_Expanse'),
    path('splite_wise/Update_Expanse/<int:pk>/',ExpanseUpdateView.as_view(),name='Update_Expanse'),

    path('splite_wise/Settil_Up/',Add_settileupView.as_view(),name='settil_Up'),
    path('splite_wise/Settil_List/',SettilementListView.as_view(),name='settil_List'), 
    # path('splite_wise/Settil_Detail/<int:pk>/',SettilementDetails.as_view(),name='settil_Details'),
    path('splite_wise/Settil_Update/<int:pk>/',SettilmentUpdate.as_view(),name='settil_Update'),#########
    path('splite_wise/Settil_Delete/<int:pk>/',SettilmentDelete.as_view(),name='settil_Delete'), ########

    path('splite_wise/Forgot/',ForgetPasswordView.as_view(),name='forgot'),
    path('splite_wise/OTP/',OtpVerify.as_view(),name='OTP'),
    path('splite_wise/Reset/',ResetPasswordView.as_view(),name='reset'),
    path('splite_wise/Premium/',PremiumView.as_view(),name="premium"),
    path('splite_wise/Success/',PaymentSuccessView.as_view(),name="Success"),
    path('splite_wise/profile/',profileView.as_view(),name="profile"),########
    path('splite_wise/profile_edit/',profile_updateView.as_view(),name="profile_update"),#########user_balances
    path('splite_wise/balance/',BlancesView.as_view(),name="user_balances")
]
