from flask import Flask, request, render_template, redirect
import os
import random
import psycopg2

app = Flask(__name__)

db_host = os.environ.get('DBHOST')
db_name = os.environ.get('DBNAME')
db_port = os.environ.get('DBPORT')
db_user = os.environ.get('DBUSER')
db_pass = os.environ.get('DBPASS')


conn = psycopg2.connect(dbname=db_name, 
                        host=db_host, 
                        port=(db_port if db_port else 5432), 
                        user=db_user, 
                        password=db_pass)

cursor = conn.cursor()

def create_sentance(words_list):
    words_list = words_list.split(',')
    random.shuffle(words_list)
    return ' '.join(words_list)
    


@app.route('/', methods=['POST', 'GET'])
def index():
    think = None
    if request.method == 'POST':
        words_list = request.form.get('words_list')
        if request.form.get('autogenerate'):
            count = int(request.form.get('auto_count'))
            for _ in range(count):
                sentance = create_sentance(words_list)
                print(sentance)
                think = 'You really think that i was create dynamically refreshed page. Oh, sorry =)'
                if db_name and db_host and db_user and db_pass:
                    query = "INSERT INTO sentances (sen) VALUES('{0}')".format(sentance)
                    cursor.execute(query)
                else:
                    raise 'DBError: error with connection to the database'
        else:
            sentance = create_sentance(words_list)
        return render_template('index.html', sentance=sentance, think=think)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)