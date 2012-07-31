# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'DailyStatus.date'
        db.alter_column('status_dailystatus', 'date', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50))

        # Adding unique constraint on 'DailyStatus', fields ['date']
        db.create_unique('status_dailystatus', ['date'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'DailyStatus', fields ['date']
        db.delete_unique('status_dailystatus', ['date'])

        # Changing field 'DailyStatus.date'
        db.alter_column('status_dailystatus', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))


    models = {
        'status.dailystatus': {
            'Meta': {'object_name': 'DailyStatus'},
            'daily_visitors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['status']
