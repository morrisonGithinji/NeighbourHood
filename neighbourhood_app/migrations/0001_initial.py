# Generated by Django 3.1.2 on 2020-11-05 06:28

import cloudinary.models
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
            name='Neighbourhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(' Kikuyu ', 'Kikuyu'), ('Dago', 'Dagoretti'), ('Karen', 'Karen'), ('Kabete', 'Kabete'), ('Kasarani', 'Kasarani'), ('Rongai', 'Rongai'), ('Westie', 'Westland'), ('Parkie', 'Parkland')], max_length=200)),
                ('location', models.CharField(default='Kenya', max_length=200)),
                ('occupants_count', models.IntegerField(default=0)),
                ('contact_police', models.CharField(default='', max_length=20)),
                ('contact_health', models.CharField(default='', max_length=20)),
                ('contact_fire', models.CharField(default='', max_length=20)),
                ('admin', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='admin_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('Bio', models.TextField()),
                ('phone_number', models.IntegerField(null=True)),
                ('neighbourhood', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neighbourhood_app.neighbourhood')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(max_length=300)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='images')),
                ('neighbourhood', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neighbourhood_app.neighbourhood')),
                ('profile', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='neighbourhood_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('neighbourhood', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neighbourhood_app.neighbourhood')),
            ],
        ),
    ]