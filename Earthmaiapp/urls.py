
# from django.contrib import admin
from django.urls import path
from Earthmaiapp import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   
    path("", views.home, name='home'),
    path('about/', views.about, name='about'),
    path('get_involved/', views.get_involved, name='get_involved'),
    # path('donate', views.donate, name='donate'),
    path('tree_plantation', views.tree_plantation, name='tree_plantation'),
    path('social', views.social, name='social'),
    path('beach', views.beach, name='beach_cleaning'),
    path('register', views.register, name='register'),
    path('login', views.userLogin, name='login'),
    path("logout",views.userLogout),
    path('initiatives_list/', views.initiatives_list, name='initiatives_list'),
    path("donate/", views.donate, name="donate"),  # Navbar link
    path("process-payment/", views.process_payment, name="process_payment"), 
    path("success/", views.success, name="success"),
    path('volunteer/', views.volunteer_form, name='volunteer_form'),
    path('success1/', views.volSuccess, name='success1'),
    path('admin1/',views.admin_dashboard, name='admin'),
    path('volunteer-details/', views.volunteer_details_view, name='volunteer-details'),
    path('partner-with-us/', views.partner_with_us, name='partner_with_us'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('enter-otp/', views.enter_otp, name='enter_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    

    # path('success/', views.success_view, name='success_V'),

    
    
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
