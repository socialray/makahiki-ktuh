# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ScoreSettings'
        db.create_table('score_mgr_scoresettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('setup_points', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('referral_bonus_points', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('active_threshold_points', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('signup_bonus_points', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('quest_bonus_points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('noshow_penalty_points', self.gf('django.db.models.fields.IntegerField')(default=4)),
        ))
        db.send_create_signal('score_mgr', ['ScoreSettings'])

        # Adding model 'ScoreboardEntry'
        db.create_table('score_mgr_scoreboardentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player_mgr.Profile'])),
            ('round_name', self.gf('django.db.models.fields.CharField')(max_length='30')),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_awarded_submission', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('score_mgr', ['ScoreboardEntry'])

        # Adding unique constraint on 'ScoreboardEntry', fields ['profile', 'round_name']
        db.create_unique('score_mgr_scoreboardentry', ['profile_id', 'round_name'])

        # Adding model 'PointsTransaction'
        db.create_table('score_mgr_pointstransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
            ('transaction_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('score_mgr', ['PointsTransaction'])

        # Adding unique constraint on 'PointsTransaction', fields ['user', 'transaction_date', 'message']
        db.create_unique('score_mgr_pointstransaction', ['user_id', 'transaction_date', 'message'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PointsTransaction', fields ['user', 'transaction_date', 'message']
        db.delete_unique('score_mgr_pointstransaction', ['user_id', 'transaction_date', 'message'])

        # Removing unique constraint on 'ScoreboardEntry', fields ['profile', 'round_name']
        db.delete_unique('score_mgr_scoreboardentry', ['profile_id', 'round_name'])

        # Deleting model 'ScoreSettings'
        db.delete_table('score_mgr_scoresettings')

        # Deleting model 'ScoreboardEntry'
        db.delete_table('score_mgr_scoreboardentry')

        # Deleting model 'PointsTransaction'
        db.delete_table('score_mgr_pointstransaction')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 8, 0, 43, 18, 449372)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 8, 0, 43, 18, 449194)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'player_mgr.profile': {
            'Meta': {'object_name': 'Profile'},
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'contact_carrier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'contact_text': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'daily_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'last_visit_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'referrer_awarded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'referring_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'referred_profiles'", 'null': 'True', 'to': "orm['auth.User']"}),
            'setup_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'setup_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Team']", 'null': 'True', 'blank': 'True'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'score_mgr.pointstransaction': {
            'Meta': {'ordering': "('-transaction_date',)", 'unique_together': "(('user', 'transaction_date', 'message'),)", 'object_name': 'PointsTransaction'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'transaction_date': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'score_mgr.scoreboardentry': {
            'Meta': {'ordering': "('round_name',)", 'unique_together': "(('profile', 'round_name'),)", 'object_name': 'ScoreboardEntry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_awarded_submission': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_mgr.Profile']"}),
            'round_name': ('django.db.models.fields.CharField', [], {'max_length': "'30'"})
        },
        'score_mgr.scoresettings': {
            'Meta': {'object_name': 'ScoreSettings'},
            'active_threshold_points': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'noshow_penalty_points': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'quest_bonus_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'referral_bonus_points': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'setup_points': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'signup_bonus_points': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        'team_mgr.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        },
        'team_mgr.team': {
            'Meta': {'object_name': 'Team'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team_mgr.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['score_mgr']
