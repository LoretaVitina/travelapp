# Generated by Django 5.0.6 on 2024-06-08 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journey', '0002_alter_event_comment_alter_event_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]
