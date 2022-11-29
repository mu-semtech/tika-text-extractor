#! /usr/bin/env sh
set -e

# /app/ping-server.sh &>/dev/null &

if [ $MODE = "development" ] ; then 
    exec python web.p
else 
    exec gunicorn -k egg:meinheld#gunicorn_worker -c "$GUNICORN_CONF" "$APP_MODULE"
fi


