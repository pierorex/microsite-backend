# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 10:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('code', models.CharField(max_length=200, verbose_name='Code')),
                ('viz_type', models.CharField(choices=[('Treemap', 'Treemap')], max_length=200, verbose_name='Visualization Type')),
                ('show_tables', models.BooleanField(default=False, verbose_name='Show Tables?')),
            ],
            options={
                'verbose_name_plural': 'Datasets',
                'verbose_name': 'Dataset',
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Hierarchies',
                'verbose_name': 'Hierarchy',
            },
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Measures',
                'verbose_name': 'Measure',
            },
        ),
        migrations.CreateModel(
            name='Microsite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('language', models.CharField(choices=[('en', 'en'), ('de', 'de'), ('es', 'es')], default='en', max_length=2, verbose_name='Language')),
                ('forum_platform', models.CharField(choices=[('Disqus', 'Disqus'), ('No', 'No')], default='Disqus', max_length=20, verbose_name='Forum')),
                ('layout', models.CharField(choices=[('datasets list, forum right', 'datasets list, forum right'), ('datasets list, forum bottom', 'datasets list, forum bottom'), ('datasets list, forum on flip', 'datasets list, forum on flip')], default='datasets list, forum right', max_length=200, verbose_name='Layout')),
                ('stacked_datasets', models.BooleanField(default=False, verbose_name='Stacked Datasets')),
            ],
            options={
                'verbose_name_plural': 'Microsites',
                'verbose_name': 'Microsite',
            },
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('country', models.CharField(max_length=200, verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'Municipalities',
                'verbose_name': 'Municipality',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vizmanager.Municipality', verbose_name='Municipality')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('brand_color', models.CharField(default='#FFFFFF', max_length=20, verbose_name='Brand Color')),
                ('sidebar_color', models.CharField(default='#888888', max_length=20, verbose_name='Sidebar Color')),
                ('content_color', models.CharField(default='#222222', max_length=20, verbose_name='Content Color')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vizmanager.Municipality', verbose_name='Municipality')),
            ],
            options={
                'verbose_name_plural': 'Themes',
                'verbose_name': 'Theme',
            },
        ),
        migrations.AddField(
            model_name='microsite',
            name='municipality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vizmanager.Municipality', verbose_name='Municipality'),
        ),
        migrations.AddField(
            model_name='microsite',
            name='selected_theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mock_microsite', to='vizmanager.Theme'),
        ),
        migrations.AddField(
            model_name='forum',
            name='microsite',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vizmanager.Microsite'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='municipality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vizmanager.Municipality', verbose_name='Municipality'),
        ),
    ]
