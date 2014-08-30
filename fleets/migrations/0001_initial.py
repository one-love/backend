# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Application'
        db.create_table(u'fleets_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('repo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
        ))
        db.send_create_signal(u'fleets', ['Application'])

        # Adding model 'Fleet'
        db.create_table(u'fleets_fleet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emailauth.CustomUser'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleets.Application'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2048)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
        ))
        db.send_create_signal(u'fleets', ['Fleet'])

        # Adding model 'BaseProvider'
        db.create_table(u'fleets_baseprovider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_fleets.baseprovider_set', null=True, to=orm['contenttypes.ContentType'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
            ('fleet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fleets.Fleet'])),
        ))
        db.send_create_signal(u'fleets', ['BaseProvider'])

        # Adding model 'AmazonProvider'
        db.create_table(u'fleets_amazonprovider', (
            (u'baseprovider_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fleets.BaseProvider'], unique=True, primary_key=True)),
            ('access_key', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('security_key', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'fleets', ['AmazonProvider'])


    def backwards(self, orm):
        # Deleting model 'Application'
        db.delete_table(u'fleets_application')

        # Deleting model 'Fleet'
        db.delete_table(u'fleets_fleet')

        # Deleting model 'BaseProvider'
        db.delete_table(u'fleets_baseprovider')

        # Deleting model 'AmazonProvider'
        db.delete_table(u'fleets_amazonprovider')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'emailauth.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'fleets.amazonprovider': {
            'Meta': {'object_name': 'AmazonProvider', '_ormbases': [u'fleets.BaseProvider']},
            'access_key': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'baseprovider_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fleets.BaseProvider']", 'unique': 'True', 'primary_key': 'True'}),
            'security_key': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'fleets.application': {
            'Meta': {'object_name': 'Application'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'repo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'})
        },
        u'fleets.baseprovider': {
            'Meta': {'object_name': 'BaseProvider'},
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleets.Fleet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_fleets.baseprovider_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'})
        },
        u'fleets.fleet': {
            'Meta': {'object_name': 'Fleet'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fleets.Application']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emailauth.CustomUser']"})
        }
    }

    complete_apps = ['fleets']