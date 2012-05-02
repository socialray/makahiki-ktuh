# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ChallengeSettings.memcached_enabled'
        db.delete_column('challenge_mgr_challengesettings', 'memcached_enabled')


    def backwards(self, orm):
        
        # Adding field 'ChallengeSettings.memcached_enabled'
        db.add_column('challenge_mgr_challengesettings', 'memcached_enabled', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


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
            'landing_introduction': ('django.db.models.fields.TextField', [], {'default': "'Aloha!'", 'max_length': '500'}),
            'landing_non_participant_text': ('django.db.models.fields.TextField', [], {'default': "'About'", 'max_length': '255'}),
            'landing_participant_text': ('django.db.models.fields.TextField', [], {'default': "'Let me in'", 'max_length': '255'}),
            'landing_slogan': ('django.db.models.fields.TextField', [], {'default': "'The Kukui Cup: Lights out, game on!'", 'max_length': '255'}),
            'landing_sponsors': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '255'}),
            'site_domain': ('django.db.models.fields.CharField', [], {'default': "'kukuicup.manoa.hawaii.edu'", 'max_length': '100'}),
            'site_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'default': "'University of Hawaii at Manoa'", 'max_length': '50'}),
            'term_conditions': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '4095'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '50'})
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
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 9, 0, 37, 10, 778395)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Round 1'", 'max_length': '50'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 2, 0, 37, 10, 778341)'})
        }
    }

    complete_apps = ['challenge_mgr']
