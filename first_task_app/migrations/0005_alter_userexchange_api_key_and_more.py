# Generated by Django 4.0.3 on 2022-04-04 01:08

from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('first_task_app', '0004_alter_userexchange_portfolio_calc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexchange',
            name='api_key',
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True),
        ),
        migrations.AlterField(
            model_name='userexchange',
            name='secret_key',
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True),
        ),
    ]
