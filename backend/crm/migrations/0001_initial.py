# Generated by Django 4.0.4 on 2022-04-29 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Имя')),
                ('position', models.CharField(max_length=64, verbose_name='Должность')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название задачи')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст задачи')),
                ('deadline', models.DateTimeField(blank=True, null=True, verbose_name='Срок исполнения')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=32, verbose_name='Номер телефона')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phones', to='crm.client', verbose_name='Клиент')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='crm.client', verbose_name='Заявка')),
            ],
        ),
    ]
