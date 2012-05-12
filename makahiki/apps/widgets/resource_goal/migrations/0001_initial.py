# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EnergyGoal'
        db.create_table('resource_goal_energygoal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('goal_status', self.gf('django.db.models.fields.CharField')(default='Not available', max_length=20)),
        ))
        db.send_create_signal('resource_goal', ['EnergyGoal'])

        # Adding unique constraint on 'EnergyGoal', fields ['team', 'date']
        db.create_unique('resource_goal_energygoal', ['team_id', 'date'])

        # Adding model 'WaterGoal'
        db.create_table('resource_goal_watergoal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('goal_status', self.gf('django.db.models.fields.CharField')(default='Not available', max_length=20)),
        ))
        db.send_create_signal('resource_goal', ['WaterGoal'])

        # Adding unique constraint on 'WaterGoal', fields ['team', 'date']
        db.create_unique('resource_goal_watergoal', ['team_id', 'date'])

        # Adding model 'EnergyGoalSetting'
        db.create_table('resource_goal_energygoalsetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('goal_percent_reduction', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('warning_percent_reduction', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('goal_points', self.gf('django.db.models.fields.IntegerField')(default=20)),
            ('manual_entry', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('manual_entry_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('resource_goal', ['EnergyGoalSetting'])

        # Adding unique constraint on 'EnergyGoalSetting', fields ['team']
        db.create_unique('resource_goal_energygoalsetting', ['team_id'])

        # Adding model 'WaterGoalSetting'
        db.create_table('resource_goal_watergoalsetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('goal_percent_reduction', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('warning_percent_reduction', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('goal_points', self.gf('django.db.models.fields.IntegerField')(default=20)),
            ('manual_entry', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('manual_entry_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('resource_goal', ['WaterGoalSetting'])

        # Adding unique constraint on 'WaterGoalSetting', fields ['team']
        db.create_unique('resource_goal_watergoalsetting', ['team_id'])

        # Adding model 'EnergyBaselineDaily'
        db.create_table('resource_goal_energybaselinedaily', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('resource_goal', ['EnergyBaselineDaily'])

        # Adding unique constraint on 'EnergyBaselineDaily', fields ['team', 'day']
        db.create_unique('resource_goal_energybaselinedaily', ['team_id', 'day'])

        # Adding model 'WaterBaselineDaily'
        db.create_table('resource_goal_waterbaselinedaily', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('resource_goal', ['WaterBaselineDaily'])

        # Adding unique constraint on 'WaterBaselineDaily', fields ['team', 'day']
        db.create_unique('resource_goal_waterbaselinedaily', ['team_id', 'day'])

        # Adding model 'EnergyBaselineHourly'
        db.create_table('resource_goal_energybaselinehourly', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
            ('hour', self.gf('django.db.models.fields.IntegerField')()),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('resource_goal', ['EnergyBaselineHourly'])

        # Adding unique constraint on 'EnergyBaselineHourly', fields ['team', 'day', 'hour']
        db.create_unique('resource_goal_energybaselinehourly', ['team_id', 'day', 'hour'])

        # Adding model 'WaterBaselineHourly'
        db.create_table('resource_goal_waterbaselinehourly', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
            ('hour', self.gf('django.db.models.fields.IntegerField')()),
            ('usage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('resource_goal', ['WaterBaselineHourly'])

        # Adding unique constraint on 'WaterBaselineHourly', fields ['team', 'day', 'hour']
        db.create_unique('resource_goal_waterbaselinehourly', ['team_id', 'day', 'hour'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'WaterBaselineHourly', fields ['team', 'day', 'hour']
        db.delete_unique('resource_goal_waterbaselinehourly', ['team_id', 'day', 'hour'])

        # Removing unique constraint on 'EnergyBaselineHourly', fields ['team', 'day', 'hour']
        db.delete_unique('resource_goal_energybaselinehourly', ['team_id', 'day', 'hour'])

        # Removing unique constraint on 'WaterBaselineDaily', fields ['team', 'day']
        db.delete_unique('resource_goal_waterbaselinedaily', ['team_id', 'day'])

        # Removing unique constraint on 'EnergyBaselineDaily', fields ['team', 'day']
        db.delete_unique('resource_goal_energybaselinedaily', ['team_id', 'day'])

        # Removing unique constraint on 'WaterGoalSetting', fields ['team']
        db.delete_unique('resource_goal_watergoalsetting', ['team_id'])

        # Removing unique constraint on 'EnergyGoalSetting', fields ['team']
        db.delete_unique('resource_goal_energygoalsetting', ['team_id'])

        # Removing unique constraint on 'WaterGoal', fields ['team', 'date']
        db.delete_unique('resource_goal_watergoal', ['team_id', 'date'])

        # Removing unique constraint on 'EnergyGoal', fields ['team', 'date']
        db.delete_unique('resource_goal_energygoal', ['team_id', 'date'])

        # Deleting model 'EnergyGoal'
        db.delete_table('resource_goal_energygoal')

        # Deleting model 'WaterGoal'
        db.delete_table('resource_goal_watergoal')

        # Deleting model 'EnergyGoalSetting'
        db.delete_table('resource_goal_energygoalsetting')

        # Deleting model 'WaterGoalSetting'
        db.delete_table('resource_goal_watergoalsetting')

        # Deleting model 'EnergyBaselineDaily'
        db.delete_table('resource_goal_energybaselinedaily')

        # Deleting model 'WaterBaselineDaily'
        db.delete_table('resource_goal_waterbaselinedaily')

        # Deleting model 'EnergyBaselineHourly'
        db.delete_table('resource_goal_energybaselinehourly')

        # Deleting model 'WaterBaselineHourly'
        db.delete_table('resource_goal_waterbaselinehourly')


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
            'date': ('django.db.models.fields.DateField', [], {}),
            'goal_status': ('django.db.models.fields.CharField', [], {'default': "'Not available'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"})
        },
        'resource_goal.energygoalsetting': {
            'Meta': {'ordering': "('team',)", 'unique_together': "(('team',),)", 'object_name': 'EnergyGoalSetting'},
            'goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'goal_points': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_entry': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'manual_entry_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'warning_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '3'})
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
            'date': ('django.db.models.fields.DateField', [], {}),
            'goal_status': ('django.db.models.fields.CharField', [], {'default': "'Not available'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"})
        },
        'resource_goal.watergoalsetting': {
            'Meta': {'ordering': "('team',)", 'unique_together': "(('team',),)", 'object_name': 'WaterGoalSetting'},
            'goal_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'goal_points': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manual_entry': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'manual_entry_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'warning_percent_reduction': ('django.db.models.fields.IntegerField', [], {'default': '3'})
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
