# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Level'
        db.create_table('smartgrid_level', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('unlock_condition', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('unlock_condition_text', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
        ))
        db.send_create_signal('smartgrid', ['Level'])

        # Adding model 'Category'
        db.create_table('smartgrid_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, db_index=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('smartgrid', ['Category'])

        # Adding model 'TextPromptQuestion'
        db.create_table('smartgrid_textpromptquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Action'])),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('smartgrid', ['TextPromptQuestion'])

        # Adding model 'QuestionChoice'
        db.create_table('smartgrid_questionchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.TextPromptQuestion'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Action'])),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('smartgrid', ['QuestionChoice'])

        # Adding model 'ConfirmationCode'
        db.create_table('smartgrid_confirmationcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Action'])),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('smartgrid', ['ConfirmationCode'])

        # Adding model 'Action'
        db.create_table('smartgrid_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('video_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('video_source', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('embedded_widget', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Level'], null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Category'], null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=1000)),
            ('pub_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 6, 8))),
            ('expire_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('unlock_condition', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('unlock_condition_text', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('related_resource', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('social_bonus', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_canopy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_group', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('point_value', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('smartgrid', ['Action'])

        # Adding model 'Commitment'
        db.create_table('smartgrid_commitment', (
            ('action_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['smartgrid.Action'], unique=True, primary_key=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('smartgrid', ['Commitment'])

        # Adding model 'Activity'
        db.create_table('smartgrid_activity', (
            ('action_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['smartgrid.Action'], unique=True, primary_key=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('point_range_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('point_range_end', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('confirm_type', self.gf('django.db.models.fields.CharField')(default='text', max_length=20)),
            ('confirm_prompt', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('smartgrid', ['Activity'])

        # Adding model 'Event'
        db.create_table('smartgrid_event', (
            ('action_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['smartgrid.Action'], unique=True, primary_key=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('event_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('event_location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('event_max_seat', self.gf('django.db.models.fields.IntegerField')(default=1000)),
        ))
        db.send_create_signal('smartgrid', ['Event'])

        # Adding model 'ActionMember'
        db.create_table('smartgrid_actionmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Action'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.TextPromptQuestion'], null=True, blank=True)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('completion_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('award_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('approval_status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=20)),
            ('social_bonus_awarded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('social_email', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('social_email2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('response', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('admin_comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=1024, blank=True)),
            ('points_awarded', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('smartgrid', ['ActionMember'])

        # Adding unique constraint on 'ActionMember', fields ['user', 'action', 'submission_date']
        db.create_unique('smartgrid_actionmember', ['user_id', 'action_id', 'submission_date'])

        # Adding model 'EmailReminder'
        db.create_table('smartgrid_emailreminder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Action'])),
            ('send_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('smartgrid', ['EmailReminder'])

        # Adding unique constraint on 'EmailReminder', fields ['user', 'action']
        db.create_unique('smartgrid_emailreminder', ['user_id', 'action_id'])

        # Adding model 'TextReminder'
        db.create_table('smartgrid_textreminder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartgrid.Action'])),
            ('send_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('text_number', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('text_carrier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('smartgrid', ['TextReminder'])

        # Adding unique constraint on 'TextReminder', fields ['user', 'action']
        db.create_unique('smartgrid_textreminder', ['user_id', 'action_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'TextReminder', fields ['user', 'action']
        db.delete_unique('smartgrid_textreminder', ['user_id', 'action_id'])

        # Removing unique constraint on 'EmailReminder', fields ['user', 'action']
        db.delete_unique('smartgrid_emailreminder', ['user_id', 'action_id'])

        # Removing unique constraint on 'ActionMember', fields ['user', 'action', 'submission_date']
        db.delete_unique('smartgrid_actionmember', ['user_id', 'action_id', 'submission_date'])

        # Deleting model 'Level'
        db.delete_table('smartgrid_level')

        # Deleting model 'Category'
        db.delete_table('smartgrid_category')

        # Deleting model 'TextPromptQuestion'
        db.delete_table('smartgrid_textpromptquestion')

        # Deleting model 'QuestionChoice'
        db.delete_table('smartgrid_questionchoice')

        # Deleting model 'ConfirmationCode'
        db.delete_table('smartgrid_confirmationcode')

        # Deleting model 'Action'
        db.delete_table('smartgrid_action')

        # Deleting model 'Commitment'
        db.delete_table('smartgrid_commitment')

        # Deleting model 'Activity'
        db.delete_table('smartgrid_activity')

        # Deleting model 'Event'
        db.delete_table('smartgrid_event')

        # Deleting model 'ActionMember'
        db.delete_table('smartgrid_actionmember')

        # Deleting model 'EmailReminder'
        db.delete_table('smartgrid_emailreminder')

        # Deleting model 'TextReminder'
        db.delete_table('smartgrid_textreminder')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 8, 0, 44, 51, 736311)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 8, 0, 44, 51, 736127)'}),
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
        'notifications.usernotification': {
            'Meta': {'object_name': 'UserNotification'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_alert': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        'smartgrid.action': {
            'Meta': {'object_name': 'Action'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Category']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'embedded_widget': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_canopy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Level']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'point_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 6, 8)'}),
            'related_resource': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'social_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'unlock_condition_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['smartgrid.ActionMember']", 'symmetrical': 'False'}),
            'video_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'video_source': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'smartgrid.actionmember': {
            'Meta': {'unique_together': "(('user', 'action', 'submission_date'),)", 'object_name': 'ActionMember'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'admin_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'approval_status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '20'}),
            'award_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'completion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'blank': 'True'}),
            'points_awarded': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.TextPromptQuestion']", 'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'social_bonus_awarded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'social_email': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'social_email2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'smartgrid.activity': {
            'Meta': {'object_name': 'Activity', '_ormbases': ['smartgrid.Action']},
            'action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid.Action']", 'unique': 'True', 'primary_key': 'True'}),
            'confirm_prompt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'confirm_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '20'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'point_range_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'point_range_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'smartgrid.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        },
        'smartgrid.commitment': {
            'Meta': {'object_name': 'Commitment', '_ormbases': ['smartgrid.Action']},
            'action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid.Action']", 'unique': 'True', 'primary_key': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        'smartgrid.confirmationcode': {
            'Meta': {'object_name': 'ConfirmationCode'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'smartgrid.emailreminder': {
            'Meta': {'unique_together': "(('user', 'action'),)", 'object_name': 'EmailReminder'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_at': ('django.db.models.fields.DateTimeField', [], {}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'smartgrid.event': {
            'Meta': {'object_name': 'Event', '_ormbases': ['smartgrid.Action']},
            'action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid.Action']", 'unique': 'True', 'primary_key': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'event_max_seat': ('django.db.models.fields.IntegerField', [], {'default': '1000'})
        },
        'smartgrid.level': {
            'Meta': {'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'unlock_condition_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'})
        },
        'smartgrid.questionchoice': {
            'Meta': {'object_name': 'QuestionChoice'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.TextPromptQuestion']"})
        },
        'smartgrid.textpromptquestion': {
            'Meta': {'object_name': 'TextPromptQuestion'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'smartgrid.textreminder': {
            'Meta': {'unique_together': "(('user', 'action'),)", 'object_name': 'TextReminder'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid.Action']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_at': ('django.db.models.fields.DateTimeField', [], {}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text_carrier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'text_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['smartgrid']
