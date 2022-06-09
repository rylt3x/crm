from django.urls import path
from . import views


urlpatterns = [
    path('delete_order/<int:pk>', views.delete_order),
    path('delete_task/<int:pk>', views.delete_task),

    path('update_task/<int:pk>', views.complete_task),

    path('orders/create', views.create_order),
    path('tasks/create', views.create_task),
    path('comment/create', views.create_comment),

    path('send_mail', views.send_mail_view)
]