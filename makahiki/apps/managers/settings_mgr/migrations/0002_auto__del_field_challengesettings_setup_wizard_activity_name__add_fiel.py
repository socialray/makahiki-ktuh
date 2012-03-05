# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ChallengeSettings.setup_wizard_activity_name'
        db.delete_column('settings_mgr_challengesettings', 'setup_wizard_activity_name')

        # Adding field 'ChallengeSettings.facebook_app_id'
        db.add_column('settings_mgr_challengesettings', 'facebook_app_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Adding field 'ChallengeSettings.facebook_secret_key'
        db.add_column('settings_mgr_challengesettings', 'facebook_secret_key', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Adding field 'ChallengeSettings.email_enabled'
        db.add_column('settings_mgr_challengesettings', 'email_enabled', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'ChallengeSettings.email_host'
        db.add_column('settings_mgr_challengesettings', 'email_host', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Adding field 'ChallengeSettings.email_port'
        db.add_column('settings_mgr_challengesettings', 'email_port', self.gf('django.db.models.fields.IntegerField')(default=587), keep_default=False)

        # Adding field 'ChallengeSettings.email_host_user'
        db.add_column('settings_mgr_challengesettings', 'email_host_user', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Adding field 'ChallengeSettings.email_host_password'
        db.add_column('settings_mgr_challengesettings', 'email_host_password', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Adding field 'ChallengeSettings.email_use_tls'
        db.add_column('settings_mgr_challengesettings', 'email_use_tls', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'ChallengeSettings.setup_wizard_activity_name'
        db.add_column('settings_mgr_challengesettings', 'setup_wizard_activity_name', self.gf('django.db.models.fields.CharField')(default='Intro video', max_length=100), keep_default=False)

        # Deleting field 'ChallengeSettings.facebook_app_id'
        db.delete_column('settings_mgr_challengesettings', 'facebook_app_id')

        # Deleting field 'ChallengeSettings.facebook_secret_key'
        db.delete_column('settings_mgr_challengesettings', 'facebook_secret_key')

        # Deleting field 'ChallengeSettings.email_enabled'
        db.delete_column('settings_mgr_challengesettings', 'email_enabled')

        # Deleting field 'ChallengeSettings.email_host'
        db.delete_column('settings_mgr_challengesettings', 'email_host')

        # Deleting field 'ChallengeSettings.email_port'
        db.delete_column('settings_mgr_challengesettings', 'email_port')

        # Deleting field 'ChallengeSettings.email_host_user'
        db.delete_column('settings_mgr_challengesettings', 'email_host_user')

        # Deleting field 'ChallengeSettings.email_host_password'
        db.delete_column('settings_mgr_challengesettings', 'email_host_password')

        # Deleting field 'ChallengeSettings.email_use_tls'
        db.delete_column('settings_mgr_challengesettings', 'email_use_tls')


    models = {
        'settings_mgr.challengesettings': {
            'Meta': {'object_name': 'ChallengeSettings'},
            'cas_server_url': ('django.db.models.fields.CharField', [], {'default': "'https://login.its.hawaii.edu/cas/'", 'max_length': '100'}),
            'competition_name': ('django.db.models.fields.CharField', [], {'default': "'Kukui Cup'", 'max_length': '50'}),
            'competition_point_label': ('django.db.models.fields.CharField', [], {'default': "'point'", 'max_length': '50'}),
            'competition_team_label': ('django.db.models.fields.CharField', [], {'default': "'Lounge'", 'max_length': '50'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_host': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'email_host_password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'email_host_user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'email_port': ('django.db.models.fields.IntegerField', [], {'default': '587'}),
            'email_use_tls': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'facebook_app_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'facebook_secret_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '50'}),
            'locale_setting': ('django.db.models.fields.CharField', [], {'default': "'en_US.UTF-8'", 'max_length': '50'}),
            'site_name': ('django.db.models.fields.CharField', [], {'default': "'University of Hawaii at Manoa'", 'max_length': '50'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '50'}),
            'time_zone': ('django.db.models.fields.CharField', [], {'default': "'Pacific/Honolulu'", 'max_length': '50'})
        },
        'settings_mgr.pagesettings': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'widget'),)", 'object_name': 'PageSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50'}),
            'widget': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50'})
        },
        'settings_mgr.roundsettings': {
            'Meta': {'ordering': "['start']", 'object_name': 'RoundSettings'},
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 12, 0, 41, 43, 764239)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Round 1'", 'max_length': '50'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 5, 0, 41, 43, 764170)'})
        }
    }

    complete_apps = ['settings_mgr']
