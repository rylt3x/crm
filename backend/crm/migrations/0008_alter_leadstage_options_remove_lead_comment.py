# Generated by Django 4.0.4 on 2022-05-04 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_remove_task_text_leadcomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leadstage',
            options={'ordering': ('stage_ordering',), 'verbose_name': 'Этап сделки', 'verbose_name_plural': 'Этапы сделки'},
        ),
        migrations.RemoveField(
            model_name='lead',
            name='comment',
        ),
    ]
