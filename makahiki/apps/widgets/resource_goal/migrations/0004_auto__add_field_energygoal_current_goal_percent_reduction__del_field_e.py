# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'EnergyGoal.current_goal_percent_reduction'
        db.add_column('resource_goal_energygoal', 'current_goal_percent_reduction', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'EnergyGoalSetting.warning_percent_reduction'
        db.delete_column('resource_goal_energygoalsetting', 'warning_percent_reduction')

        # Deleting field 'EnergyGoalSetting.power_meter_interval'
        db.delete_column('resource_goal_energygoalsetting', 'power_meter_interval')

        # Adding field 'EnergyGoalSetting.baseline_method'
        db.add_column('resource_goal_energygoalsetting', 'baseline_method', self.gf('django.db.models.fields.CharField')(default='Dynamic', max_length=20), keep_default=False)

        # Adding field 'EnergyGoalSetting.realtime_meter_interval'
        db.add_column('resource_goal_energygoalsetting', 'realtime_meter_interval', self.gf('django.db.models.fields.IntegerField')(default=10), keep_default=False)

        # Deleting field 'WaterGoalSetting.warning_percent_reduction'
        db.delete_column('resource_goal_watergoalsetting', 'warning_percent_reduction')

        # Adding field 'WaterGoalSetting.baseline_method'
        db.add_column('resource_goal_watergoalsetting', 'baseline_method', self.gf('django.db.models.fields.CharField')(default='Dynamic', max_length=20), keep_default=False)

        # Adding field 'WaterGoalSetting.realtime_meter_interval'
        db.add_column('resource_goal_watergoalsetting', 'realtime_meter_interval', self.gf('django.db.models.fields.IntegerField')(default=10), keep_default=False)

        # Adding field 'WaterGoal.current_goal_percent_reduction'
        db.add_column('resource_goal_watergoal', 'current_goal_percent_reduction', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'EnergyGoal.current_goal_percent_reduction'
        db.delete_column('resource_goal_energygoal', 'current_goal_percent_reduction')

        # Adding field 'EnergyGoalSetting.warning_percent_reduction'
        db.add_column('resource_goal_energygoalsetting', 'warning_percent_reduction', self.gf('django.db.models.fields.IntegerField')(default=3), keep_default=False)

        # Adding field 'EnergyGoalSetting.power_meter_interval'
        db.add_column('resource_goal_energygoalsetting', 'power_meter_interval', self.gf('django.db.models.fields.IntegerField')(default=10), keep_default=False)

        # Deleting field 'EnergyGoalSetting.baseline_method'
        db.delete_column('resource_goal_energygoalsetting', 'baseline_method')

        # Deleting field 'EnergyGoalSetting.realtime_meter_interval'
        db.delete_column('resource_goal_energygoalsetting', 'realtime_meter_interval')

        # Adding field 'WaterGoalSetting.warning_percent_reduction'
        db.add_column('resource_goal_watergoalsetting', 'warning_percent_reduction', self.gf('django.db.models.fields.IntegerField')(default=3), keep_default=False)

        # Deleting field 'WaterGoalSetting.baseline_method'
        db.delete_column('resource_goal_watergoalsetting', 'baseline_method')

        # Deleting field 'WaterGoalSetting.realtime_meter_interval'
        db.delete_column('resource_goal_watergoalsetting', 'realtime_meter_interval')

        # Deleting field 'WaterGoal.current_goal_percent_reduction'
        db.delete_column('resource_goal_watergoal', 'current_goal_percent_reduction')


    models = {
        'resource_goal.energybaselinedaily': {
            'Meta': {'ordering': "('team', 'day')", 'unique_together': "(('team', 'day'),)", 'object_name': 'EnergyBaselineDaily'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_goal.energybaselinehourly': {
            'Meta': {'ordering': "('team', 'day', 'hour')", 'unique_together': "(('team', 'day', 'hour'),)", 'object_name': 'EnergyBaselineHourly'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'hour': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_goal.energygoal': {
            'Meta': {'ordering': "('team', 'date')", 'unique_together': "(('team', 'date'),)", 'object_name': 'EnergyGoal'},
            'current_goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'goal_status': ('django.db.models.fields.CharField', [], {'default': "'Not available'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"})
        },
        'resource_goal.energygoalsetting': {
            'Meta': {'ordering': "('team',)", 'unique_together': "(('team',),)", 'object_name': 'EnergyGoalSetting'},
            'baseline_method': ('django.db.models.fields.CharField', [], {'default': "'Dynamic'", 'max_length': '20'}),
            'goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'goal_points': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_entry': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'manual_entry_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'realtime_meter_interval': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"})
        },
        'resource_goal.waterbaselinedaily': {
            'Meta': {'ordering': "('team', 'day')", 'unique_together': "(('team', 'day'),)", 'object_name': 'WaterBaselineDaily'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_goal.waterbaselinehourly': {
            'Meta': {'ordering': "('team', 'day', 'hour')", 'unique_together': "(('team', 'day', 'hour'),)", 'object_name': 'WaterBaselineHourly'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'hour': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'resource_goal.watergoal': {
            'Meta': {'ordering': "('team', 'date')", 'unique_together': "(('team', 'date'),)", 'object_name': 'WaterGoal'},
            'current_goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'goal_status': ('django.db.models.fields.CharField', [], {'default': "'Not available'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"})
        },
        'resource_goal.watergoalsetting': {
            'Meta': {'ordering': "('team',)", 'unique_together': "(('team',),)", 'object_name': 'WaterGoalSetting'},
            'baseline_method': ('django.db.models.fields.CharField', [], {'default': "'Dynamic'", 'max_length': '20'}),
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
            'Meta': {'object_name': 'Team'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['resource_goal']
