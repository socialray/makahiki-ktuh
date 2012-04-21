# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ChallengeSettings'
        db.create_table('challenge_mgr_challengesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_name', self.gf('django.db.models.fields.CharField')(default='University of Hawaii at Manoa', max_length=50)),
            ('competition_name', self.gf('django.db.models.fields.CharField')(default='Kukui Cup', max_length=50)),
            ('competition_team_label', self.gf('django.db.models.fields.CharField')(default='Lounge', max_length=50)),
            ('cas_server_url', self.gf('django.db.models.fields.CharField')(default='https://login.its.hawaii.edu/cas/', max_length=100)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('theme', self.gf('django.db.models.fields.CharField')(default='default', max_length=50)),
            ('facebook_app_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('facebook_secret_key', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('email_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_host', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('email_port', self.gf('django.db.models.fields.IntegerField')(default=587)),
            ('email_use_tls', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('challenge_mgr', ['ChallengeSettings'])

        # Adding model 'RoundSettings'
        db.create_table('challenge_mgr_roundsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Round 1', max_length=50)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 4, 21, 1, 16, 20, 373050))),
            ('end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 4, 28, 1, 16, 20, 373104))),
        ))
        db.send_create_signal('challenge_mgr', ['RoundSettings'])

        # Adding model 'PageSettings'
        db.create_table('challenge_mgr_pagesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='home', max_length=50)),
            ('widget', self.gf('django.db.models.fields.CharField')(default='home', max_length=50)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('challenge_mgr', ['PageSettings'])

        # Adding unique constraint on 'PageSettings', fields ['name', 'widget']
        db.create_unique('challenge_mgr_pagesettings', ['name', 'widget'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PageSettings', fields ['name', 'widget']
        db.delete_unique('challenge_mgr_pagesettings', ['name', 'widget'])

        # Deleting model 'ChallengeSettings'
        db.delete_table('challenge_mgr_challengesettings')

        # Deleting model 'RoundSettings'
        db.delete_table('challenge_mgr_roundsettings')

        # Deleting model 'PageSettings'
        db.delete_table('challenge_mgr_pagesettings')


    models = {
        'challenge_mgr.challengesettings': {
            'Meta': {'object_name': 'ChallengeSettings'},
            'cas_server_url': ('django.db.models.fields.CharField', [], {'default': "'https://login.its.hawaii.edu/cas/'", 'max_length': '100'}),
            'competition_name': ('django.db.models.fields.CharField', [], {'default': "'Kukui Cup'", 'max_length': '50'}),
            'competition_team_label': ('django.db.models.fields.CharField', [], {'default': "'Lounge'", 'max_length': '50'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_host': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'email_port': ('django.db.models.fields.IntegerField', [], {'default': '587'}),
            'email_use_tls': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'facebook_app_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'facebook_secret_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'default': "'University of Hawaii at Manoa'", 'max_length': '50'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '50'})
        },
        'challenge_mgr.pagesettings': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'widget'),)", 'object_name': 'PageSettings'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50'}),
            'widget': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50'})
        },
        'challenge_mgr.roundsettings': {
            'Meta': {'ordering': "['start']", 'object_name': 'RoundSettings'},
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 28, 1, 16, 20, 373104)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Round 1'", 'max_length': '50'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 21, 1, 16, 20, 373050)'})
        }
    }

    complete_apps = ['challenge_mgr']
