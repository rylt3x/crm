from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from .utils import send_mail

from . import serializers

from crm import models
from crm import forms



@api_view(['POST'])
def create_order(request, *args, **kwargs):
    order_form = forms.OrderForm(request.POST)
    if order_form.is_valid():
        order_form.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_order(request, *args, **kwargs):
    pk = kwargs.get('pk')
    try:
        obj = models.Lead.objects.get(pk=pk).delete()
    except models.Lead.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_task(request, **kwargs):
    task_form = forms.TaskForm(request.POST)
    if task_form.is_valid():
        task_obj = task_form.save()
        return Response(status=status.HTTP_200_OK, data={'name': task_obj.name, 'deadline': task_obj.deadline})
    return Response(status=status.HTTP_400_BAD_REQUEST, data=task_form.errors)


@api_view(['POST'])
def create_comment(request, **kwargs):
    comment_form = forms.LeadCommentForm(request.POST)
    if comment_form.is_valid():
        comment_obj = comment_form.save()
        return Response(status=status.HTTP_200_OK, data={'name': comment_obj.text})
    return Response(status=status.HTTP_400_BAD_REQUEST, data=comment_form.errors)


@api_view(['DELETE'])
def delete_task(request, *args, **kwargs):
    pk = kwargs.get('pk')
    try:
        obj = models.Task.objects.get(pk=pk).delete()
    except models.Task.DoesNotExist as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['UPDATE'])
def complete_task(request, *args, **kwargs):
    pk = kwargs.get('pk')
    try:
        obj = models.Task.objects.get(pk=pk)
        obj.is_done = True
        obj.save()
    except models.Task.DoesNotExist as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def send_mail_view(request, *args, **kwargs):
    receiver = request.POST.get('receiver')
    subject = request.POST.get('subject')
    mail_text = request.POST.get('mail_text')

    if not receiver:
        return Response(data={'message': 'Subject or receiver is empty'}, status=status.HTTP_400_BAD_REQUEST)

    send_mail(mail_text, subject, receiver)

    return Response(status=status.HTTP_200_OK)
