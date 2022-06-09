from django.contrib import admin
from django.urls import path, include
from crm import views as crm_views
from crm.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm/', include(('crm.urls', 'crm'), namespace='crm')),
    path('api/v1/', include('api.urls')),
    path('accounts/login/', crm_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', crm_views.LogoutView.as_view(), name='logout'),
]
