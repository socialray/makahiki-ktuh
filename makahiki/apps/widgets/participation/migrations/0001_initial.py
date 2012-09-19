# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ParticipationSetting'
        db.create_table('participation_participationsetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('points_50_percent', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('points_75_percent', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('points_100_percent', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('participation', ['ParticipationSetting'])

        # Adding model 'TeamParticipation'
        db.create_table('participation_teamparticipation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team_mgr.Team'])),
            ('participation', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('participation', ['TeamParticipation'])


    def backwards(self, orm):
        
        # Deleting model 'ParticipationSetting'
        db.delete_table('participation_participationsetting')

        # Deleting model 'TeamParticipation'
        db.delete_table('participation_teamparticipation')


    models = {
        'participation.participationsetting': {
            'Meta': {'object_name': 'ParticipationSetting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_100_percent': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'points_50_percent': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'points_75_percent': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        'participation.teamparticipation': {
            'Meta': {'ordering': "['-participation']", 'object_name': 'TeamParticipation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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

    complete_apps = ['participation']
