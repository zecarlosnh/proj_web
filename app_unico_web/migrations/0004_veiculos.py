# Generated by Django 4.2.6 on 2023-12-21 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_unico_web', '0003_alter_caminhos_arquivos_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Veiculos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('modelo', models.TextField()),
                ('placa', models.TextField()),
            ],
        ),
    ]
