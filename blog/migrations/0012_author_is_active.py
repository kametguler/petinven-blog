# Generated by Django 3.2.15 on 2022-10-03 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Aktif mi ?'),
        ),
    ]
