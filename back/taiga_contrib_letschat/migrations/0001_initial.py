# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20150311_0821'),
    ]

    operations = [
        migrations.CreateModel(
            name='LetsChatHook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('token', models.CharField(max_length=200, verbose_name='Token')),
                ('project', models.ForeignKey(related_name='letschathooks', to='projects.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
