# Generated by Django 3.1.2 on 2022-02-14 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('initial_account_balance', models.IntegerField()),
                ('account_balance', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('trade_type', models.CharField(choices=[('B', 'Buy'), ('S', 'Sell')], max_length=1)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('stock_symbol', models.CharField(max_length=255)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='portfolio.portfolio')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
