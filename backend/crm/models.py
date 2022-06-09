from django.db import models
import datetime
import re


class LeadStage(models.Model):
    stage_name = models.CharField(verbose_name='Название этапа', max_length=64)
    stage_ordering = models.IntegerField(verbose_name='Порядковый номер')

    def __str__(self):
        return f'{self.stage_name}'

    class Meta:
        verbose_name = 'Этап сделки'
        verbose_name_plural = 'Этапы сделки'
        ordering = ('stage_ordering',)


class Lead(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128, null=True, blank=True)
    budget = models.IntegerField(verbose_name='Бюджет', default=0)
    stage = models.ForeignKey(LeadStage, on_delete=models.SET_NULL, related_name='leads', verbose_name='Этап сделки',
                              null=True, blank=True)
    client = models.ForeignKey(to='Client', related_name='leads', verbose_name='Клиент', on_delete=models.SET_NULL,
                               null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    @property
    def last_task(self):
        return self.tasks.filter(is_done=False).order_by('-created_at').first()

    @property
    def get_lead_name(self):
        if self.name:
            return f'{self.name}'
        return f'Сделка #{self.id}'

    @property
    def get_separated_budget(self):
        return f'{self.budget:,}₽'.replace(',', ' ')

    def __str__(self):
        return f'{str(self.name)[:10]} | {str(self.client)}'

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'


class Client(models.Model):
    client_name = models.CharField(verbose_name='Имя', max_length=64, null=True, blank=True)
    client_phone_number = models.CharField(verbose_name='Номер телефона', max_length=32, null=True, blank=True)
    client_email = models.EmailField(verbose_name='Email', null=True, blank=True)
    client_position = models.CharField(verbose_name='Должность', max_length=64, null=True, blank=True)
    client_comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def save(self, *args, **kwargs):
        self.client_phone_number = re.sub('\D', '', str(self.client_phone_number))
        super(Client, self).save(*args, **kwargs)

    @property
    def pretty_phone(self):
        if self.client_phone_number:
            code = self.client_phone_number[0]
            sub_code = self.client_phone_number[1:4]
            after_code = self.client_phone_number[4:7]
            pre_last = self.client_phone_number[7:9]
            last = self.client_phone_number[9:]
            phone_number = f'+{code} ({sub_code}) {after_code}-{pre_last}-{last}'
            return phone_number
        return self.client_phone_number

    @property
    def avatar_symbols(self):
        if self.client_name:
            text = self.client_name.split(' ')
            symbols = [x[0].upper() for x in text][:2]
            if len(symbols) < 2:
                symbols.append('N')
            return ''.join(symbols)

    def __str__(self):
        return f'{self.client_name} | {self.client_phone_number}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Task(models.Model):
    name = models.CharField(verbose_name='Название задачи', max_length=64)
    to_lead = models.ForeignKey(Lead, models.CASCADE, verbose_name='Отношение к задаче', related_name='tasks',
                                null=True, blank=True)
    deadline = models.DateTimeField(verbose_name='Срок исполнения', null=True, blank=True)
    is_done = models.BooleanField(verbose_name='Выполнена', default=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    @property
    def event_type(self):
        return 'task'

    @property
    def check_if_overdued(self):
        if self.deadline:
            if datetime.datetime.now().timestamp() > self.deadline.timestamp():
                return True
            return False
        return None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class LeadComment(models.Model):
    to_lead = models.ForeignKey(Lead, models.CASCADE, related_name='comments', verbose_name='Относится к сделке')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    @property
    def event_type(self):
        return 'comment'

    def __str__(self):
        return f'{self.to_lead.name} | {self.text}'

    class Meta:
        verbose_name = 'Комментарий к сделке'
        verbose_name_plural = 'Комментарии к сделке'
