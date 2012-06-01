# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ChallengeSettings.use_facebook'
        db.delete_column('challenge_mgr_challengesettings', 'use_facebook')

        # Adding field 'ChallengeSettings.cas_auth_text'
        db.add_column('challenge_mgr_challengesettings', 'cas_auth_text', self.gf('django.db.models.fields.TextField')(default='###I have a CAS email', max_length=255), keep_default=False)

        # Adding field 'ChallengeSettings.ldap_auth_text'
        db.add_column('challenge_mgr_challengesettings', 'ldap_auth_text', self.gf('django.db.models.fields.TextField')(default='###I have a LDAP email', max_length=255), keep_default=False)

        # Adding field 'ChallengeSettings.internal_auth_text'
        db.add_column('challenge_mgr_challengesettings', 'internal_auth_text', self.gf('django.db.models.fields.TextField')(default='###Others', max_length=255), keep_default=False)

        # Changing field 'ChallengeSettings.email_host'
        db.alter_column('challenge_mgr_challengesettings', 'email_host', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'ChallengeSettings.contact_email'
        db.alter_column('challenge_mgr_challengesettings', 'contact_email', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))


    def backwards(self, orm):
        
        # Adding field 'ChallengeSettings.use_facebook'
        db.add_column('challenge_mgr_challengesettings', 'use_facebook', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'ChallengeSettings.cas_auth_text'
        db.delete_column('challenge_mgr_challengesettings', 'cas_auth_text')

        # Deleting field 'ChallengeSettings.ldap_auth_text'
        db.delete_column('challenge_mgr_challengesettings', 'ldap_auth_text')

        # Deleting field 'ChallengeSettings.internal_auth_text'
        db.delete_column('challenge_mgr_challengesettings', 'internal_auth_text')

        # Changing field 'ChallengeSettings.email_host'
        db.alter_column('challenge_mgr_challengesettings', 'email_host', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'ChallengeSettings.contact_email'
        db.alter_column('challenge_mgr_challengesettings', 'contact_email', self.gf('django.db.models.fields.CharField')(default=1, max_length=100))


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
            'theme': ('django.db.models.fields.CharField', [], {'default': "'theme-default'", 'max_length': '50'}),
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
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 7, 14, 8, 55, 787500)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Round 1'", 'max_length': '50'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 31, 14, 8, 55, 787440)'})
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
