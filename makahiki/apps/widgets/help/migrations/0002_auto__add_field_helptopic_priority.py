# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'HelpTopic.priority'
        db.add_column('help_helptopic', 'priority', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'HelpTopic.priority'
        db.delete_column('help_helptopic', 'priority')


    models = {
        'help.helptopic': {
            'Meta': {'object_name': 'HelpTopic'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_topic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_topics'", 'null': 'True', 'to': "orm['help.HelpTopic']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['help']
