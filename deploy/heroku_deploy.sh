heroku run python makahiki/manage.py syncdb --noinput

heroku run python makahiki/manage.py loaddata makahiki/fixtures/base_teams.json
heroku run python makahiki/manage.py loaddata makahiki/fixtures/test_users.json 
heroku run python makahiki/manage.py loaddata makahiki/fixtures/base_activities.json 
heroku run python makahiki/manage.py loaddata makahiki/fixtures/base_quests.json 
heroku run python makahiki/manage.py loaddata makahiki/fixtures/base_help.json 
heroku run python makahiki/manage.py loaddata makahiki/fixtures/test_posts.json
heroku run python makahiki/manage.py loaddata makahiki/fixtures/test_prizes.json 
