# Generated by Django 2.1.7 on 2019-12-11 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('context', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(default='', max_length=200)),
                ('type', models.IntegerField(choices=[(0, 'Bronze'), (1, 'Silver'), (2, 'Gold')], default=0)),
                ('unique', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=0)),
                ('icon', models.CharField(default='fa fa-asterisk', max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='award',
            name='badge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badges.Badge'),
        ),
        migrations.AddField(
            model_name='award',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
