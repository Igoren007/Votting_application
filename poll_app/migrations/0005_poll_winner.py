# Generated by Django 4.0.4 on 2022-05-25 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll_app', '0004_alter_poll_date_end_alter_poll_date_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner', to='poll_app.person'),
        ),
    ]
