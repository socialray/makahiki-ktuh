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
            ('site_name', self.gf('django.db.models.fields.CharField')(default='My site', max_length=50)),
            ('site_domain', self.gf('django.db.models.fields.CharField')(default='localhost', max_length=100)),
            ('site_logo', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('competition_name', self.gf('django.db.models.fields.CharField')(default='Kukui Cup', max_length=50)),
            ('theme', self.gf('django.db.models.fields.CharField')(default='theme-forest', max_length=50)),
            ('competition_team_label', self.gf('django.db.models.fields.CharField')(default='Team', max_length=50)),
            ('use_cas_auth', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cas_server_url', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('cas_auth_text', self.gf('django.db.models.fields.TextField')(default='###I have a CAS email', max_length=255)),
            ('use_ldap_auth', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ldap_server_url', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('ldap_search_base', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('ldap_auth_text', self.gf('django.db.models.fields.TextField')(default='###I have a LDAP email', max_length=255)),
            ('use_internal_auth', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('internal_auth_text', self.gf('django.db.models.fields.TextField')(default='###Others', max_length=255)),
            ('wattdepot_server_url', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email_host', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email_port', self.gf('django.db.models.fields.IntegerField')(default=587)),
            ('email_use_tls', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('landing_slogan', self.gf('django.db.models.fields.TextField')(default='The Kukui Cup: Lights out, game on!', max_length=255)),
            ('landing_introduction', self.gf('django.db.models.fields.TextField')(default='Aloha! Welcome to the Kukui Cup.', max_length=500)),
            ('landing_participant_text', self.gf('django.db.models.fields.TextField')(default='###I am registered', max_length=255)),
            ('landing_non_participant_text', self.gf('django.db.models.fields.TextField')(default='###I am not registered.', max_length=255)),
            ('about_page_text', self.gf('django.db.models.fields.TextField')(default="For more information, please go to <a href='http://kukuicup.org'>kukuicup.org</a>.")),
        ))
        db.send_create_signal('challenge_mgr', ['ChallengeSettings'])

        # Adding model 'Sponsor'
        db.create_table('challenge_mgr_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenge_mgr.ChallengeSettings'])),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default='1')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('logo_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('challenge_mgr', ['Sponsor'])

        # Adding model 'RoundSettings'
        db.create_table('challenge_mgr_roundsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Round 1', max_length=50)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 8, 0, 42, 35, 208782))),
            ('end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 15, 0, 42, 35, 208836))),
        ))
        db.send_create_signal('challenge_mgr', ['RoundSettings'])

        # Adding model 'PageInfo'
        db.create_table('challenge_mgr_pageinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('introduction', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('url', self.gf('django.db.models.fields.CharField')(default='/', max_length=255)),
            ('unlock_condition', self.gf('django.db.models.fields.CharField')(default='True', max_length=255)),
        ))
        db.send_create_signal('challenge_mgr', ['PageInfo'])

        # Adding model 'PageSettings'
        db.create_table('challenge_mgr_pagesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenge_mgr.PageInfo'])),
            ('widget', self.gf('django.db.models.fields.CharField')(default='home', max_length=50)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('challenge_mgr', ['PageSettings'])

        # Adding unique constraint on 'PageSettings', fields ['page', 'widget']
        db.create_unique('challenge_mgr_pagesettings', ['page_id', 'widget'])

        # Adding model 'UploadImage'
        db.create_table('challenge_mgr_uploadimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('challenge_mgr', ['UploadImage'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PageSettings', fields ['page', 'widget']
        db.delete_unique('challenge_mgr_pagesettings', ['page_id', 'widget'])

        # Deleting model 'ChallengeSettings'
        db.delete_table('challenge_mgr_challengesettings')

        # Deleting model 'Sponsor'
        db.delete_table('challenge_mgr_sponsor')

        # Deleting model 'RoundSettings'
        db.delete_table('challenge_mgr_roundsettings')

        # Deleting model 'PageInfo'
        db.delete_table('challenge_mgr_pageinfo')

        # Deleting model 'PageSettings'
        db.delete_table('challenge_mgr_pagesettings')

        # Deleting model 'UploadImage'
        db.delete_table('challenge_mgr_uploadimage')


    models = {
        'challenge_mgr.challengesettings': {
            'Meta': {'object_name': 'ChallengeSettings'},
            'about_page_text': ('django.db.models.fields.TextField', [], {'default': '"For more information, please go to <a href=\'http://kukuicup.org\'>kukuicup.org</a>."'}),
            'cas_auth_text': ('django.db.models.fields.TextField', [], {'default': "'###I have a CAS email'", 'max_length': '255'}),
            'cas_server_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'competition_name': ('django.db.models.fields.CharField', [], {'default': "'Kukui Cup'", 'max_length': '50'}),
            'competition_team_label': ('django.db.models.fields.CharField', [], {'default': "'Team'", 'max_length': '50'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_host': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_port': ('django.db.models.fields.IntegerField', [], {'default': '587'}),
            'email_use_tls': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_auth_text': ('django.db.models.fields.TextField', [], {'default': "'###Others'", 'max_length': '255'}),
            'landing_introduction': ('django.db.models.fields.TextField', [], {'default': "'Aloha! Welcome to the Kukui Cup.'", 'max_length': '500'}),
            'landing_non_participant_text': ('django.db.models.fields.TextField', [], {'default': "'###I am not registered.'", 'max_length': '255'}),
            'landing_participant_text': ('django.db.models.fields.TextField', [], {'default': "'###I am registered'", 'max_length': '255'}),
            'landing_slogan': ('django.db.models.fields.TextField', [], {'default': "'The Kukui Cup: Lights out, game on!'", 'max_length': '255'}),
            'ldap_auth_text': ('django.db.models.fields.TextField', [], {'default': "'###I have a LDAP email'", 'max_length': '255'}),
            'ldap_search_base': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ldap_server_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_domain': ('django.db.models.fields.CharField', [], {'default': "'localhost'", 'max_length': '100'}),
            'site_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'default': "'My site'", 'max_length': '50'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "'theme-forest'", 'max_length': '50'}),
            'use_cas_auth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_internal_auth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_ldap_auth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wattdepot_server_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'challenge_mgr.pageinfo': {
            'Meta': {'object_name': 'PageInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'default': "'True'", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "'/'", 'max_length': '255'})
        },
        'challenge_mgr.pagesettings': {
            'Meta': {'ordering': "['page', 'widget']", 'unique_together': "(('page', 'widget'),)", 'object_name': 'PageSettings'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge_mgr.PageInfo']"}),
            'widget': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50'})
        },
        'challenge_mgr.roundsettings': {
            'Meta': {'ordering': "['start']", 'object_name': 'RoundSettings'},
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 15, 0, 42, 35, 208836)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Round 1'", 'max_length': '50'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 8, 0, 42, 35, 208782)'})
        },
        'challenge_mgr.sponsor': {
            'Meta': {'ordering': "['priority', 'name']", 'object_name': 'Sponsor'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge_mgr.ChallengeSettings']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'logo_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': "'1'"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'challenge_mgr.uploadimage': {
            'Meta': {'object_name': 'UploadImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['challenge_mgr']
