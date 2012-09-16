# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'EnergyGoalSetting.data_storage'
        db.add_column('resource_goal_energygoalsetting', 'data_storage', self.gf('django.db.models.fields.CharField')(default='Wattdepot', max_length=20), keep_default=False)

        # Adding field 'WaterGoalSetting.data_storage'
        db.add_column('resource_goal_watergoalsetting', 'data_storage', self.gf('django.db.models.fields.CharField')(default='Wattdepot', max_length=20), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'EnergyGoalSetting.data_storage'
        db.delete_column('resource_goal_energygoalsetting', 'data_storage')

        # Deleting field 'WaterGoalSetting.data_storage'
        db.delete_column('resource_goal_watergoalsetting', 'data_storage')


    models = {
        'resource_goal.energybaselinedaily': {
            'Meta': {'object_name': 'EnergyBaselineDaily'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_goal.energybaselinehourly': {
            'Meta': {'object_name': 'EnergyBaselineHourly'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'hour': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_goal.energygoal': {
            'Meta': {'ordering': "('-date', 'team')", 'unique_together': "(('date', 'team'),)", 'object_name': 'EnergyGoal'},
            'actual_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'baseline_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'goal_status': ('django.db.models.fields.CharField', [], {'default': "'Not available'", 'max_length': '20'}),
            'goal_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 15, 13, 22, 47, 457009)', 'auto_now': 'True', 'blank': 'True'})
        },
        'resource_goal.energygoalsetting': {
            'Meta': {'ordering': "('team',)", 'unique_together': "(('team',),)", 'object_name': 'EnergyGoalSetting'},
            'baseline_method': ('django.db.models.fields.CharField', [], {'default': "'Dynamic'", 'max_length': '20'}),
            'data_storage': ('django.db.models.fields.CharField', [], {'default': "'Wattdepot'", 'max_length': '20'}),
            'goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'goal_points': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_entry': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'manual_entry_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'realtime_meter_interval': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"})
        },
        'resource_goal.waterbaselinedaily': {
            'Meta': {'object_name': 'WaterBaselineDaily'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_goal.waterbaselinehourly': {
            'Meta': {'object_name': 'WaterBaselineHourly'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'hour': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_goal.watergoal': {
            'Meta': {'ordering': "('-date', 'team')", 'unique_together': "(('date', 'team'),)", 'object_name': 'WaterGoal'},
            'actual_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'baseline_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'goal_status': ('django.db.models.fields.CharField', [], {'default': "'Not available'", 'max_length': '20'}),
            'goal_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 15, 13, 22, 47, 457009)', 'auto_now': 'True', 'blank': 'True'})
        },
        'resource_goal.watergoalsetting': {
            'Meta': {'ordering': "('team',)", 'unique_together': "(('team',),)", 'object_name': 'WaterGoalSetting'},
            'baseline_method': ('django.db.models.fields.CharField', [], {'default': "'Dynamic'", 'max_length': '20'}),
            'data_storage': ('django.db.models.fields.CharField', [], {'default': "'Wattdepot'", 'max_length': '20'}),
            'goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'goal_points': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_entry': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'manual_entry_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'realtime_meter_interval': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"})
        },
        'team_mgr.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        },
        'team_mgr.team': {
            'Meta': {'ordering': "('group', 'name')", 'object_name': 'Team'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['resource_goal']
