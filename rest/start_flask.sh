sleep 30  # dummy way to wait for postgres DB to start
flask db init
flask db migrate
flask db upgrade
flask run