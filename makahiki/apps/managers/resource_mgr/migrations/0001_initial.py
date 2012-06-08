# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ResourceSettings'
        db.create_table('resource_mgr_resourcesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('winning_order', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('resource_mgr', ['ResourceSettings'])

        # Adding unique constraint on 'ResourceSettings', fields ['name']
        db.create_unique('resource_mgr_resourcesettings', ['name'])

        # Adding model 'EnergyUsage'
        db.create_table('resource_mgr_energyusage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('resource_mgr', ['EnergyUsage'])

        # Adding unique constraint on 'EnergyUsage', fields ['date', 'team']
        db.create_unique('resource_mgr_energyusage', ['date', 'team_id'])

        # Adding model 'WaterUsage'
        db.create_table('resource_mgr_waterusage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('resource_mgr', ['WaterUsage'])

        # Adding unique constraint on 'WaterUsage', fields ['date', 'team']
        db.create_unique('resource_mgr_waterusage', ['date', 'team_id'])

        # Adding model 'WasteUsage'
        db.create_table('resource_mgr_wasteusage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('resource_mgr', ['WasteUsage'])

        # Adding unique constraint on 'WasteUsage', fields ['date', 'team']
        db.create_unique('resource_mgr_wasteusage', ['date', 'team_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'WasteUsage', fields ['date', 'team']
        db.delete_unique('resource_mgr_wasteusage', ['date', 'team_id'])

        # Removing unique constraint on 'WaterUsage', fields ['date', 'team']
        db.delete_unique('resource_mgr_waterusage', ['date', 'team_id'])

        # Removing unique constraint on 'EnergyUsage', fields ['date', 'team']
        db.delete_unique('resource_mgr_energyusage', ['date', 'team_id'])

        # Removing unique constraint on 'ResourceSettings', fields ['name']
        db.delete_unique('resource_mgr_resourcesettings', ['name'])

        # Deleting model 'ResourceSettings'
        db.delete_table('resource_mgr_resourcesettings')

        # Deleting model 'EnergyUsage'
        db.delete_table('resource_mgr_energyusage')

        # Deleting model 'WaterUsage'
        db.delete_table('resource_mgr_waterusage')

        # Deleting model 'WasteUsage'
        db.delete_table('resource_mgr_wasteusage')


    models = {
        'resource_mgr.energyusage': {
            'Meta': {'ordering': "('date', 'team')", 'unique_together': "(('date', 'team'),)", 'object_name': 'EnergyUsage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_mgr.resourcesettings': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'ResourceSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'winning_order': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'resource_mgr.wasteusage': {
            'Meta': {'ordering': "('date', 'team')", 'unique_together': "(('date', 'team'),)", 'object_name': 'WasteUsage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_mgr.waterusage': {
            'Meta': {'ordering': "('date', 'team')", 'unique_together': "(('date', 'team'),)", 'object_name': 'WaterUsage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'time': ('django.db.models.fields.TimeField', [], {}),
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
