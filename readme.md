make migrations
python -m manager db migrate

apply migrations
python -m manager db upgrade