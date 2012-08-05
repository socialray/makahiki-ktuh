# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'BonusPoints'
        db.delete_table('bonus_points_bonuspoints')

        # Adding model 'BonusPoint'
        db.create_table('bonus_points_bonuspoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('point_value', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('bonus_points', ['BonusPoint'])


    def backwards(self, orm):
        
        # Adding model 'BonusPoints'
        db.create_table('bonus_points_bonuspoints', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('point_value', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('bonus_points', ['BonusPoints'])

        # Deleting model 'BonusPoint'
        db.delete_table('bonus_points_bonuspoint')


    models = {
        'bonus_points.bonuspoint': {
            'Meta': {'object_name': 'BonusPoint'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'point_value': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        }
    }

    complete_apps = ['bonus_points']
