# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('ssh_key', models.TextField(null=True, verbose_name='private SSH key', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('repo', models.CharField(unique=True, max_length=256)),
                ('playbook', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('url', models.CharField(unique=True, max_length=2048)),
                ('group', models.ForeignKey(related_name='fleets', to='auth.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('ssh_user', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=64, choices=[(b'awsprovider', b'Amazon Web Services'), (b'sshprovider', b'SSH')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AWSProvider',
            fields=[
                ('provider_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='onelove.Provider')),
                ('access_key', models.CharField(max_length=256)),
                ('security_key', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=('onelove.provider',),
        ),
        migrations.CreateModel(
            name='SSHHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SSHProvider',
            fields=[
                ('provider_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='onelove.Provider')),
            ],
            options={
            },
            bases=('onelove.provider',),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', uuidfield.fields.UUIDField(max_length=32, serialize=False, primary_key=True)),
                ('fleet', models.ForeignKey(related_name='tasks', to='onelove.Fleet')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sshhost',
            name='ssh_provider',
            field=models.ForeignKey(related_name='hosts', to='onelove.SSHProvider'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='provider',
            name='fleet',
            field=models.ForeignKey(related_name='providers', to='onelove.Fleet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='fleet',
            field=models.ForeignKey(related_name='applications', to='onelove.Fleet'),
            preserve_default=True,
        ),
    ]
