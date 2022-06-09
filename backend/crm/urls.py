from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.CrmView.as_view(), name='main_page'),
    path('orders/list', views.OrderListView.as_view(), name='order_list'),
    path('orders/create', views.OrderCreateView.as_view(), name='create_order'),
    path('orders/update/<int:pk>', views.OrderUpdateView.as_view(), name='update_order'),

    path('tasks/list', views.TaskListView.as_view(), name='task_list'),
]