# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'EnergyUsage.manual_meter_reading'
        db.add_column('resource_mgr_energyusage', 'manual_meter_reading', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'WaterUsage.manual_meter_reading'
        db.add_column('resource_mgr_waterusage', 'manual_meter_reading', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'WasteUsage.manual_meter_reading'
        db.add_column('resource_mgr_wasteusage', 'manual_meter_reading', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'EnergyUsage.manual_meter_reading'
        db.delete_column('resource_mgr_energyusage', 'manual_meter_reading')

        # Deleting field 'WaterUsage.manual_meter_reading'
        db.delete_column('resource_mgr_waterusage', 'manual_meter_reading')

        # Deleting field 'WasteUsage.manual_meter_reading'
        db.delete_column('resource_mgr_wasteusage', 'manual_meter_reading')


    models = {
        'resource_mgr.energyusage': {
            'Meta': {'ordering': "('date', 'team')", 'unique_together': "(('date', 'team'),)", 'object_name': 'EnergyUsage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 6, 28)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_meter_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 37, 53, 79199)'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_mgr.resourcesetting': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'ResourceSetting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'winning_order': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'resource_mgr.wasteusage': {
            'Meta': {'ordering': "('date', 'team')", 'unique_together': "(('date', 'team'),)", 'object_name': 'WasteUsage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 6, 28)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_meter_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 37, 53, 79199)'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_mgr.waterusage': {
            'Meta': {'ordering': "('date', 'team')", 'unique_together': "(('date', 'team'),)", 'object_name': 'WaterUsage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 6, 28)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_meter_reading': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 37, 53, 79199)'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'team_mgr.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        },
        'team_mgr.team': {
            'Meta': {'object_name': 'Team'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['resource_mgr']
