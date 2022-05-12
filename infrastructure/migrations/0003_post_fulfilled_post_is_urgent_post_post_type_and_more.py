# Generated by Django 4.0.1 on 2022-05-12 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0002_alter_organization_tags_alter_profile_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='fulfilled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='is_urgent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('n', 'needer'), ('h', 'helper')], default='n', max_length=1),
        ),
        migrations.AlterField(
            model_name='subjecttag',
            name='verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='verified',
            field=models.BooleanField(default=True),
        ),
    ]
