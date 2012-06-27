# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DailyStatus'
        db.create_table('status_dailystatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('daily_visitors', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('status', ['DailyStatus'])


    def backwards(self, orm):
        
        # Deleting model 'DailyStatus'
        db.delete_table('status_dailystatus')


    models = {
        'status.dailystatus': {
            'Meta': {'object_name': 'DailyStatus'},
            'daily_visitors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['status']
