# Generated by Django 4.2.9 on 2024-04-19 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(verbose_name='Age')),
                ('fullname', models.CharField(blank=True, max_length=100, null=True, verbose_name='fullname')),
                ('Registered_date', models.DateField(auto_now_add=True, verbose_name='Registered date')),
                ('Updated_date', models.DateField(auto_now=True, verbose_name='Updated date')),
            ],
            options={
                'verbose_name': 'Student',
            },
        ),
    ]
