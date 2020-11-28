# Generated by Django 3.1.3 on 2020-11-28 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0002_auto_20201110_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone_number', models.TextField()),
                ('booking_start_date', models.DateField()),
                ('booking_end_date', models.DateField()),
                ('booking_message', models.TextField()),
                ('is_approved', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='car/images')),
                ('description', models.TextField()),
                ('daily_rent', models.IntegerField()),
                ('is_available', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.RemoveField(
            model_name='webpage',
            name='topic',
        ),
        migrations.DeleteModel(
            name='AccessRecord',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.DeleteModel(
            name='Webpage',
        ),
        migrations.AddField(
            model_name='booking',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.car'),
        ),
    ]