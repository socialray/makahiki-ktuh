# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Prize'
        db.create_table('prizes_prize', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('short_description', self.gf('django.db.models.fields.TextField')()),
            ('long_description', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=1024, blank=True)),
            ('round_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('award_to', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('competition_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('prizes', ['Prize'])

        # Adding unique constraint on 'Prize', fields ['round_name', 'award_to', 'competition_type']
        db.create_unique('prizes_prize', ['round_name', 'award_to', 'competition_type'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Prize', fields ['round_name', 'award_to', 'competition_type']
        db.delete_unique('prizes_prize', ['round_name', 'award_to', 'competition_type'])

        # Deleting model 'Prize'
        db.delete_table('prizes_prize')


    models = {
        'prizes.prize': {
            'Meta': {'unique_together': "(('round_name', 'award_to', 'competition_type'),)", 'object_name': 'Prize'},
            'award_to': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'competition_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'blank': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {}),
            'round_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'short_description': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['prizes']
