# Generated by Django 4.2.6 on 2023-12-26 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_unico_web', '0005_alter_veiculos_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Motoristas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.TextField()),
            ],
            options={
                'db_table': 'motoristas',
            },
        ),
    ]
