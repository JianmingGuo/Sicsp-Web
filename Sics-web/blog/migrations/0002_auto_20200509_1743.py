# Generated by Django 3.0.5 on 2020-05-09 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogtype',
            name='type_name',
            field=models.CharField(max_length=50),
        ),
    ]
