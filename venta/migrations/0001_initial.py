# Generated by Django 4.2.6 on 2023-10-12 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pokedexNumber', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('element', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hp', models.IntegerField()),
                ('attack', models.IntegerField()),
                ('defense', models.IntegerField()),
                ('speed', models.IntegerField()),
                ('image_url', models.URLField()),
            ],
        ),
    ]
