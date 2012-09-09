# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'DailyStatus.setup_users'
        db.add_column('status_dailystatus', 'setup_users', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'DailyStatus.short_date'
        db.add_column('status_dailystatus', 'short_date', self.gf('django.db.models.fields.DateField')(null=True), keep_default=False)

        # Adding field 'DailyStatus.updated_at'
        db.add_column('status_dailystatus', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'DailyStatus.setup_users'
        db.delete_column('status_dailystatus', 'setup_users')

        # Deleting field 'DailyStatus.short_date'
        db.delete_column('status_dailystatus', 'short_date')

        # Deleting field 'DailyStatus.updated_at'
        db.delete_column('status_dailystatus', 'updated_at')


    models = {
        'status.dailystatus': {
            'Meta': {'object_name': 'DailyStatus'},
            'daily_visitors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'setup_users': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'short_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['status']
