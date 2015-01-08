# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogengine', '0005_auto_20150108_2205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='descriptions',
            new_name='description',
        ),
    ]
