
# script to deploy to heroku.
# command parameter: $1 -- the instance name, e.g., hpu, ewc
# currently it deploy to staging, it could be paramtered to production etc.

heroku create makahiki-staging-$1 --stack cedar --remote heroku-$1

git push heroku-$1 master

AWS_STORAGE_BUCKET_NAME=makahiki-$1

heroku config:add --app makahiki-staging-$1 MAKAHIKI_ADMIN_INFO=$MAKAHIKI_ADMIN_INFO \
    MAKAHIKI_MEMCACHED_ENABLED=$MAKAHIKI_MEMCACHED_ENABLED \
    MAKAHIKI_USE_S3=$MAKAHIKI_USE_S3 \
    AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME

heroku addons:add --app makahiki-staging-$1 memcache

heroku run --app makahiki-staging-$1 python makahiki/manage.py syncdb --noinput

heroku run --app makahiki-staging-$1 python makahiki/manage.py migrate

heroku run --app makahiki-staging-$1 python makahiki/manage.py loaddata makahiki/fixtures/base*.json
heroku run --app makahiki-staging-$1 python makahiki/manage.py loaddata makahiki/fixtures/test*.json

heroku run --app makahiki-staging-$1 python makahiki/manage.py setup_test_data

heroku run --app makahiki-staging-$1 python makahiki/manage.py update_energy_usage
