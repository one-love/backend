# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fleet'
        db.create_table(u'fleets_fleet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('hosting', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('repo', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'fleets', ['Fleet'])


    def backwards(self, orm):
        # Deleting model 'Fleet'
        db.delete_table(u'fleets_fleet')


    models = {
        u'fleets.fleet': {
            'Meta': {'object_name': 'Fleet'},
            'hosting': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['fleets']