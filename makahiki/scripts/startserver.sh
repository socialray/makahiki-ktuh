rm dev.db
python manage.py syncdb --noinput
python manage.py migrate
scripts/load_data.sh
