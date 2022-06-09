# Generated by Django 4.0.4 on 2022-04-30 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_client_email_client_phone_number_alter_lead_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='to_lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='crm.lead', verbose_name='Отношение к задаче'),
        ),
    ]
