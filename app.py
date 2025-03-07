from flask import Flask, request, jsonify, render_template
import psycopg2,os
from psycopg2 import sql

#Get Env Variables
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

# POSTGRES SQL ENV
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")


app = Flask(__name__)

#App Routing

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
	try:
        	conn = psycopg2.connect(dbname = POSTGRES_DB, user = POSTGRES_USER,password = POSTGRES_PW, host = POSTGRES_URL, port=5432)
	except:
        	print("I am unable to connect to the database.")
	cur = conn.cursor()
	#c = cur.execute("INSERT INTO pathcount(path,count) VALUES (%s,1) on CONFLICT(path) DO UPDATE  SET count = pathcount.count + 1  RETURNING count;",(path,))
	c = cur.execute(sql.SQL("INSERT INTO {} VALUES (%s,1) on CONFLICT(path) DO UPDATE  SET count = pathcount.count + 1  RETURNING count;").format(sql.Identifier('pathcount')),[path,])
	try:
		cur.execute("SELECT * from pathcount ORDER BY path;")
	except:
		print("cant print out pathcount")
	rows = cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()
	#for row in rows:
	#	print(row[0])
	return render_template("index.html",rows = rows)
	#return "ok"

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080)


