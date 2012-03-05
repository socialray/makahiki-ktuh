heroku run python makahiki/manage.py syncdb --noinput
heroku run python makahiki/manage.py migrate
heroku run python makahiki/manage.py loaddata makahiki/fixtures/base_*.json
