# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'HourlyWaterBaseline', fields ['team', 'day', 'hour']
        db.delete_unique('resource_mgr_hourlywaterbaseline', ['team_id', 'day', 'hour'])

        # Removing unique constraint on 'DailyWaterBaseline', fields ['team', 'day']
        db.delete_unique('resource_mgr_dailywaterbaseline', ['team_id', 'day'])

        # Removing unique constraint on 'DailyEnergyBaseline', fields ['team', 'day']
        db.delete_unique('resource_mgr_dailyenergybaseline', ['team_id', 'day'])

        # Removing unique constraint on 'HourlyEnergyBaseline', fields ['team', 'day', 'hour']
        db.delete_unique('resource_mgr_hourlyenergybaseline', ['team_id', 'day', 'hour'])

        # Deleting model 'HourlyEnergyBaseline'
        db.delete_table('resource_mgr_hourlyenergybaseline')

        # Deleting model 'DailyEnergyBaseline'
        db.delete_table('resource_mgr_dailyenergybaseline')

        # Deleting model 'DailyWaterBaseline'
        db.delete_table('resource_mgr_dailywaterbaseline')

        # Deleting model 'HourlyWaterBaseline'
        db.delete_table('resource_mgr_hourlywaterbaseline')


    def backwards(self, orm):
        
        # Adding model 'HourlyEnergyBaseline'
        db.create_table('resource_mgr_hourlyenergybaseline', (
            ('hour', self.gf('django.db.models.fields.IntegerField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('resource_mgr', ['HourlyEnergyBaseline'])

        # Adding unique constraint on 'HourlyEnergyBaseline', fields ['team', 'day', 'hour']
        db.create_unique('resource_mgr_hourlyenergybaseline', ['team_id', 'day', 'hour'])

        # Adding model 'DailyEnergyBaseline'
        db.create_table('resource_mgr_dailyenergybaseline', (
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('resource_mgr', ['DailyEnergyBaseline'])

        # Adding unique constraint on 'DailyEnergyBaseline', fields ['team', 'day']
        db.create_unique('resource_mgr_dailyenergybaseline', ['team_id', 'day'])

        # Adding model 'DailyWaterBaseline'
        db.create_table('resource_mgr_dailywaterbaseline', (
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('resource_mgr', ['DailyWaterBaseline'])

        # Adding unique constraint on 'DailyWaterBaseline', fields ['team', 'day']
        db.create_unique('resource_mgr_dailywaterbaseline', ['team_id', 'day'])

        # Adding model 'HourlyWaterBaseline'
        db.create_table('resource_mgr_hourlywaterbaseline', (
            ('hour', self.gf('django.db.models.fields.IntegerField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('resource_mgr', ['HourlyWaterBaseline'])

        # Adding unique constraint on 'HourlyWaterBaseline', fields ['team', 'day', 'hour']
        db.create_unique('resource_mgr_hourlywaterbaseline', ['team_id', 'day', 'hour'])


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
