# Generated by Django 5.1.7 on 2025-03-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_remove_article_external_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='cover_design',
        ),
        migrations.AddField(
            model_name='article',
            name='external_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
