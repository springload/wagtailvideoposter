# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0004_make_focal_point_key_not_nullable'),
        ('wagtailembeds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmbedVideoPosterImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('embed', models.ForeignKey(related_name='poster_image', to='wagtailembeds.Embed')),
                ('image', models.ForeignKey(related_name='+', blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='embedvideoposterimage',
            unique_together=set([('image', 'embed')]),
        ),
    ]
