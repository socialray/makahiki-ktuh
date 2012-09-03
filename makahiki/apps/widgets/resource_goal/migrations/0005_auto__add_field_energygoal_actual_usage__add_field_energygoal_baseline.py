# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'WaterBaselineDaily', fields ['day', 'team']
        db.delete_unique('resource_goal_waterbaselinedaily', ['day', 'team_id'])

        # Removing unique constraint on 'EnergyBaselineDaily', fields ['day', 'team']
        db.delete_unique('resource_goal_energybaselinedaily', ['day', 'team_id'])

        # Removing unique constraint on 'WaterBaselineHourly', fields ['day', 'hour', 'team']
        db.delete_unique('resource_goal_waterbaselinehourly', ['day', 'hour', 'team_id'])

        # Removing unique constraint on 'EnergyBaselineHourly', fields ['day', 'hour', 'team']
        db.delete_unique('resource_goal_energybaselinehourly', ['day', 'hour', 'team_id'])

        # Adding field 'EnergyGoal.actual_usage'
        db.add_column('resource_goal_energygoal', 'actual_usage', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'EnergyGoal.baseline_usage'
        db.add_column('resource_goal_energygoal', 'baseline_usage', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'EnergyGoal.goal_usage'
        db.add_column('resource_goal_energygoal', 'goal_usage', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'EnergyGoal.updated_at'
        db.add_column('resource_goal_energygoal', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 2, 13, 28, 32, 487705), auto_now=True, blank=True), keep_default=False)

        # Adding field 'WaterGoal.actual_usage'
        db.add_column('resource_goal_watergoal', 'actual_usage', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'WaterGoal.baseline_usage'
        db.add_column('resource_goal_watergoal', 'baseline_usage', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'WaterGoal.goal_usage'
        db.add_column('resource_goal_watergoal', 'goal_usage', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'WaterGoal.updated_at'
        db.add_column('resource_goal_watergoal', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 2, 13, 28, 32, 487705), auto_now=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'EnergyGoal.actual_usage'
        db.delete_column('resource_goal_energygoal', 'actual_usage')

        # Deleting field 'EnergyGoal.baseline_usage'
        db.delete_column('resource_goal_energygoal', 'baseline_usage')

        # Deleting field 'EnergyGoal.goal_usage'
        db.delete_column('resource_goal_energygoal', 'goal_usage')

        # Deleting field 'EnergyGoal.updated_at'
        db.delete_column('resource_goal_energygoal', 'updated_at')

        # Adding unique constraint on 'EnergyBaselineHourly', fields ['day', 'hour', 'team']
        db.create_unique('resource_goal_energybaselinehourly', ['day', 'hour', 'team_id'])

        # Adding unique constraint on 'WaterBaselineHourly', fields ['day', 'hour', 'team']
        db.create_unique('resource_goal_waterbaselinehourly', ['day', 'hour', 'team_id'])

        # Adding unique constraint on 'EnergyBaselineDaily', fields ['day', 'team']
        db.create_unique('resource_goal_energybaselinedaily', ['day', 'team_id'])

        # Adding unique constraint on 'WaterBaselineDaily', fields ['day', 'team']
        db.create_unique('resource_goal_waterbaselinedaily', ['day', 'team_id'])

        # Deleting field 'WaterGoal.actual_usage'
        db.delete_column('resource_goal_watergoal', 'actual_usage')

        # Deleting field 'WaterGoal.baseline_usage'
        db.delete_column('resource_goal_watergoal', 'baseline_usage')

        # Deleting field 'WaterGoal.goal_usage'
        db.delete_column('resource_goal_watergoal', 'goal_usage')

        # Deleting field 'WaterGoal.updated_at'
        db.delete_column('resource_goal_watergoal', 'updated_at')


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
            'Meta': {'ordering': "('team', '-date')", 'unique_together': "(('team', 'date'),)", 'object_name': 'EnergyGoal'},
            'actual_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'baseline_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'goal_status': ('django.db.models.fields.CharField', [], {'default': "'Not available'", 'max_length': '20'}),
            'goal_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 2, 13, 28, 32, 487705)', 'auto_now': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "('team', '-date')", 'unique_together': "(('team', 'date'),)", 'object_name': 'WaterGoal'},
            'actual_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'baseline_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'goal_status': ('django.db.models.fields.CharField', [], {'default': "'Not available'", 'max_length': '20'}),
            'goal_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 2, 13, 28, 32, 487705)', 'auto_now': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "('group', 'name')", 'object_name': 'Team'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['resource_goal']
