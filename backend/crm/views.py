import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url, reverse

from project import settings
from . import forms
from itertools import chain
import re

from . import models, forms


class LoginView(auth_views.LoginView):
    form_class = forms.LoginForm

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)


class LogoutView(auth_views.LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get_next_page(self):
        return reverse('login')


@method_decorator(login_required, 'dispatch')
class CrmView(TemplateView):
    template_name = 'crm/index.html'

    def get_context_data(self, **kwargs):
        context = super(CrmView, self).get_context_data(**kwargs)
        context['clients_count'] = models.Client.objects.all().count()
        context['leads'] = models.Lead.objects.all().select_related('client', 'stage')
        context['create_order_form'] = forms.OrderForm()
        context['total_budget'] = sum([price.budget if price.budget else 0 for price in context['leads']])
        return context


@method_decorator(login_required, 'dispatch')
class OrderCreateView(CreateView):
    model = models.Lead
    form_class = forms.OrderForm
    template_name = 'crm/create_order.html'

    def get_success_url(self):
        return reverse('crm:main_page')


@method_decorator(login_required, 'dispatch')
class OrderUpdateView(UpdateView):
    model = models.Lead
    template_name = 'crm/update_order.html'
    form_class = forms.OrderForm

    def get_success_url(self):
        return reverse('crm:update_order', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        client_instance = self.object.client

        if self.request.POST:
            context['client_form'] = forms.ClientForm(self.request.POST, instance=client_instance)
        else:
            context['client_form'] = forms.ClientForm(instance=client_instance)

        task_list = models.Task.objects.filter(to_lead=self.object).order_by('deadline', '-created_at')
        context['lead_tasks'] = task_list.filter(is_done=False)
        context['completed_tasks'] = task_list.filter(is_done=True).order_by('modified_at')

        context['lead_events'] = self.get_lead_events()

        return context

    # Получение ивентов
    def get_lead_events(self, *args, **kwargs):
        lead_events = {}
        today = datetime.datetime.now().date()

        lead_comments = models.LeadComment.objects.filter(to_lead=self.object)
        lead_tasks = models.Task.objects.filter(to_lead=self.object, is_done=True)

        # Комментарии на сегодня
        today_comments = lead_comments.filter(
            created_at__year=today.year,
            created_at__month=today.month,
            created_at__day=today.day
        )
        # Завершенные задачи на сегодня
        today_tasks = lead_tasks.filter(
            created_at__year=today.year,
            created_at__month=today.month,
            created_at__day=today.day
        )
        # Объединение QuerySets двух разных моделей
        today_evs = sorted(chain(
            today_tasks, today_comments
        ), key=lambda event: event.modified_at)

        # Остальные комментарии
        other_comments = lead_comments.exclude(
            created_at__year=today.year,
            created_at__month=today.month,
            created_at__day=today.day
        )
        # Остальные задачи
        other_tasks = lead_tasks.exclude(
            created_at__year=today.year,
            created_at__month=today.month,
            created_at__day=today.day
        )
        # Такое же объединение двух QuerySets
        other_evs = sorted(chain(
            other_comments, other_tasks
        ), key=lambda event: event.modified_at)

        # Раскидываем в словарь списков исходя из даты, но не времени
        for event in other_evs:
            str_time = event.created_at.strftime('%d.%m.%Y')
            if not lead_events.get(str_time):
                lead_events[str_time] = []
            lead_events[str_time].append(event)

        lead_events['today_events'] = today_evs
        return lead_events

    def form_valid(self, form):
        context = self.get_context_data()
        client_form = context['client_form']

        if client_form.is_valid():
            client = client_form.save()
            if not self.object.client:
                self.object.client = client
        self.object.save()
        return super(OrderUpdateView, self).form_valid(form)


@method_decorator(login_required, 'dispatch')
class OrderListView(ListView):
    model = models.Lead
    template_name = 'crm/order_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderListView, self).get_context_data(*args, **kwargs)
        leads = models.Lead.objects.exclude(stage__stage_ordering=2000).select_related('stage', 'client')
        context['leads'] = leads
        return context


@method_decorator(login_required, 'dispatch')
class TaskListView(ListView):
    model = models.Task
    template_name = 'crm/task_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TaskListView, self).get_context_data(*args, **kwargs)
        tasks = models.Task.objects.exclude(is_done=True).select_related('to_lead')
        context['tasks'] = tasks
        return context



