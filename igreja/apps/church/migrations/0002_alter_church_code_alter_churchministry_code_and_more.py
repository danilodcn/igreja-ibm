# Generated by Django 4.1.6 on 2023-02-16 16:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("church", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="church",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="Usado para identificar a igreja",
                max_length=30,
                null=True,
                unique=True,
                verbose_name="Código",
            ),
        ),
        migrations.AlterField(
            model_name="churchministry",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="Usado para identificar o ministério",
                max_length=30,
                null=True,
                unique=True,
                verbose_name="Código",
            ),
        ),
        migrations.AlterField(
            model_name="membertype",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="Usado para identificar o tipo de membro",
                max_length=30,
                null=True,
                unique=True,
                verbose_name="Código",
            ),
        ),
    ]
