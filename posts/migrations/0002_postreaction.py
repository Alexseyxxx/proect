# Generated by Django 5.2.1 on 2025-05-10 08:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.CharField(choices=[('like', 'Лайк'), ('dislike', 'Дизлайк')], max_length=7, verbose_name='реакция')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='posts.posts', verbose_name='статья')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_reactions', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'реакция на статью',
                'verbose_name_plural': 'реакции на статьи',
                'unique_together': {('user', 'post')},
            },
        ),
    ]
