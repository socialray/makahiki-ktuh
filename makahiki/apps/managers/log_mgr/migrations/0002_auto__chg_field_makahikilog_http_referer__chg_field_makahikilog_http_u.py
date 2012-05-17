# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'MakahikiLog.http_referer'
        db.alter_column('log_mgr_makahikilog', 'http_referer', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))

        # Changing field 'MakahikiLog.http_user_agent'
        db.alter_column('log_mgr_makahikilog', 'http_user_agent', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))


    def backwards(self, orm):
        
        # Changing field 'MakahikiLog.http_referer'
        db.alter_column('log_mgr_makahikilog', 'http_referer', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True))

        # Changing field 'MakahikiLog.http_user_agent'
        db.alter_column('log_mgr_makahikilog', 'http_user_agent', self.gf('django.db.models.fields.TextField')(max_length=300, null=True))


    models = {
        'log_mgr.makahikilog': {
            'Meta': {'object_name': 'MakahikiLog'},
            'http_referer': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'http_user_agent': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'post_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'remote_ip': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'remote_user': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'request_method': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'request_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'request_url': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'response_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['log_mgr']
