# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Prize', fields ['round_name', 'competition_type', 'award_to']
        db.delete_unique('prizes_prize', ['round_name', 'competition_type', 'award_to'])

        # Deleting field 'Prize.round_name'
        db.delete_column('prizes_prize', 'round_name')

        # Adding unique constraint on 'Prize', fields ['competition_type', 'round', 'award_to']
        db.create_unique('prizes_prize', ['competition_type', 'round_id', 'award_to'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Prize', fields ['competition_type', 'round', 'award_to']
        db.delete_unique('prizes_prize', ['competition_type', 'round_id', 'award_to'])

        # Adding field 'Prize.round_name'
        db.add_column('prizes_prize', 'round_name', self.gf('django.db.models.fields.CharField')(default='foo', max_length=50), keep_default=False)

        # Adding unique constraint on 'Prize', fields ['round_name', 'competition_type', 'award_to']
        db.create_unique('prizes_prize', ['round_name', 'competition_type', 'award_to'])


    models = {
        'challenge_mgr.roundsetting': {
            'Meta': {'ordering': "['start']", 'object_name': 'RoundSetting'},
            'display_scoreboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 8, 14, 26, 48, 314095)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Round 1'", 'max_length': '50'}),
            'round_reset': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 1, 14, 26, 48, 314028)'})
        },
        'prizes.prize': {
            'Meta': {'ordering': "('round__name', 'award_to', 'competition_type')", 'unique_together': "(('round', 'award_to', 'competition_type'),)", 'object_name': 'Prize'},
            'award_to': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'competition_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'blank': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge_mgr.RoundSetting']", 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['prizes']
