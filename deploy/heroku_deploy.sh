
# script to deploy to heroku.
# command parameter: $1 -- the instance name, e.g., makahiki-staging-uh, makahiki-prod-ewc, etc
# will use the instance name as the app name, remote name, and aws bucket name.

heroku create $1 --stack cedar --remote $1

MAKAHIKI_AWS_STORAGE_BUCKET_NAME=$1
MAKAHIKI_USE_HEROKU=True

heroku config:add --app $1 MAKAHIKI_ADMIN_INFO=$MAKAHIKI_ADMIN_INFO \
    MAKAHIKI_USE_MEMCACHED=$MAKAHIKI_USE_MEMCACHED \
    MAKAHIKI_USE_HEROKU=$MAKAHIKI_USE_HEROKU \
    MAKAHIKI_USE_S3=$MAKAHIKI_USE_S3 \
    MAKAHIKI_AWS_ACCESS_KEY_ID=$MAKAHIKI_AWS_ACCESS_KEY_ID \
    MAKAHIKI_AWS_SECRET_ACCESS_KEY=$MAKAHIKI_AWS_SECRET_ACCESS_KEY \
    MAKAHIKI_AWS_STORAGE_BUCKET_NAME=$MAKAHIKI_AWS_STORAGE_BUCKET_NAME

heroku addons:add --app $1 memcache

git push $1 master

cd makahiki

scripts/initialize_instance.py -t demo -h $1
