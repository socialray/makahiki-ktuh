web: newrelic-admin run-program python makahiki/manage.py run_gunicorn -b 0.0.0.0:$PORT -w 3
celeryd: python makahiki/manage.py celeryd -E -B --loglevel=INFO
