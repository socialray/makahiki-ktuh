# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ChallengeSettings'
        db.create_table('settings_mgr_challengesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_name', self.gf('django.db.models.fields.CharField')(default='University of Hawaii at Manoa', max_length=50)),
            ('competition_name', self.gf('django.db.models.fields.CharField')(default='Kukui Cup', max_length=50)),
            ('competition_point_label', self.gf('django.db.models.fields.CharField')(default='point', max_length=50)),
            ('competition_team_label', self.gf('django.db.models.fields.CharField')(default='Lounge', max_length=50)),
            ('cas_server_url', self.gf('django.db.models.fields.CharField')(default='https://login.its.hawaii.edu/cas/', max_length=100)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('setup_wizard_activity_name', self.gf('django.db.models.fields.CharField')(default='Intro video', max_length=100)),
            ('time_zone', self.gf('django.db.models.fields.CharField')(default='Pacific/Honolulu', max_length=50)),
            ('language_code', self.gf('django.db.models.fields.CharField')(default='en', max_length=50)),
            ('locale_setting', self.gf('django.db.models.fields.CharField')(default='en_US.UTF-8', max_length=50)),
            ('theme', self.gf('django.db.models.fields.CharField')(default='default', max_length=50)),
        ))
        db.send_create_signal('settings_mgr', ['ChallengeSettings'])

        # Adding model 'RoundSettings'
        db.create_table('settings_mgr_roundsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Round 1', max_length=50)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 3, 5, 0, 40, 21, 859582))),
            ('end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 3, 12, 0, 40, 21, 859643))),
        ))
        db.send_create_signal('settings_mgr', ['RoundSettings'])

        # Adding model 'PageSettings'
        db.create_table('settings_mgr_pagesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='home', max_length=50)),
            ('widget', self.gf('django.db.models.fields.CharField')(default='home', max_length=50)),
        ))
        db.send_create_signal('settings_mgr', ['PageSettings'])

        # Adding unique constraint on 'PageSettings', fields ['name', 'widget']
        db.create_unique('settings_mgr_pagesettings', ['name', 'widget'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PageSettings', fields ['name', 'widget']
        db.delete_unique('settings_mgr_pagesettings', ['name', 'widget'])

        # Deleting model 'ChallengeSettings'
        db.delete_table('settings_mgr_challengesettings')

        # Deleting model 'RoundSettings'
        db.delete_table('settings_mgr_roundsettings')

        # Deleting model 'PageSettings'
        db.delete_table('settings_mgr_pagesettings')


    models = {
        'settings_mgr.challengesettings': {
            'Meta': {'object_name': 'ChallengeSettings'},
            'cas_server_url': ('django.db.models.fields.CharField', [], {'default': "'https://login.its.hawaii.edu/cas/'", 'max_length': '100'}),
            'competition_name': ('django.db.models.fields.CharField', [], {'default': "'Kukui Cup'", 'max_length': '50'}),
            'competition_point_label': ('django.db.models.fields.CharField', [], {'default': "'point'", 'max_length': '50'}),
            'competition_team_label': ('django.db.models.fields.CharField', [], {'default': "'Lounge'", 'max_length': '50'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '50'}),
            'locale_setting': ('django.db.models.fields.CharField', [], {'default': "'en_US.UTF-8'", 'max_length': '50'}),
            'setup_wizard_activity_name': ('django.db.models.fields.CharField', [], {'default': "'Intro video'", 'max_length': '100'}),
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
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 12, 0, 40, 21, 859643)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Round 1'", 'max_length': '50'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 5, 0, 40, 21, 859582)'})
        }
    }

    complete_apps = ['settings_mgr']
