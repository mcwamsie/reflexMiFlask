from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import datetime
#import dateutil.relativedelta
#from newsapi import Ne

import pymysql.cursors

db = pymysql.connect(host="localhost",user='root', password='pass', database='world', cursorclass=pymysql.cursors.DictCursor)
db1 = pymysql.connect(host="localhost",user='root', password='pass', database='reflectmi', cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
#app.config['SERVER_NAME'] = '192.168.42.198:5000'

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handleNewConnection():
    print('We have a new connection')
    
    emit('calendar_update', 'New connection',broadcaast=True)

@socketio.on('update_mirror')
def handleNewConnection():
    print('Update Mirror')
    
    emit('calendar_update', 'Mirror Update',broadcaast=True)


@socketio.on('disconnect')
def handleDisconnect():
    print('User Left')

#@app.route('/news')
#def getNews():
    # Init
   # newsapi = NewsApiClient(api_key='b1240a4660ba4f8fbbaef238e7539caa')
    # /v2/top-headlines
    #top_headlines = newsapi.get_top_headlines(
     #                                     country='za'
       #                                   )
    # /v2/everything
    #all_articles = newsapi.get_everything(q='corona',
    #                                  sources='bbc-news,the-verge',
     #                                 domains='bbc.co.uk,techcrunch.com',
    #                                  from_param='2021-05-04',
    #                                  to='2021-05-05',
    #                                  language='en',
    #                                  sort_by='relevancy',
    #                                  page=2)
    #return all_articles


@app.route('/calendar/types')
def getReminderType():
    cursor = db1.cursor()
    sql = "SELECT * FROM `eventtype`"
    cursor.execute(sql)
    results = cursor.fetchall()
    data = {}
    data['items'] = results
    return data

@app.route('/calendar')
def getCalender():
    cursor = db1.cursor()
    sql = "SELECT calendar.id, calendar.dateTime, calendar.EventType, calendar.eventName, calendar.Note, eventtype.EventTypeName FROM calendar INNER JOIN eventtype ON calendar.EventType = eventtype.EventTypeId WHERE calendar.dateTime > now( )  ORDER BY calendar.dateTime ASC"
    cursor.execute(sql)
    results = cursor.fetchall()
    data = {}

    for res in results:
        t= res['dateTime'] 
        #now =datetime.datetime.now()
        ##rd = dateutil.relativedelta.relativedelta(t, now)
        
        res['dateTime'] = t.strftime("%Y/%m/%d %H:%M:%S")
       ## res['dateTime'] = t.timestamp()
    print('\n')
    print('Number of Records :', len(results))
    print(results)
    print('\n')
    data['items'] = results
    now =datetime.datetime.now()
    data['date'] = now.strftime("%d-%m-%Y %H:%M:%S")
    #send(results,broadcaast=True)
    return data


@socketio.on('message')
def handleMessage(msg):
    print('Message '+ msg)
    #send(msg, broadcaast=True)

@app.route('/')
def index():
    cursor = db.cursor()
    sql = "SELECT city.ID, city.`Name`, country.`Name` AS `Country`, city.District, city.Population, country.Continent, country.HeadOfState, country.GovernmentForm, country.Capital FROM city INNER JOIN country ON city.CountryCode = country.`Code`"
    try:

        cursor.execute(sql)
    except pymysql.Error as e:
        print('\nSQL ERROR %d: %s', e.args[0], e.args[1])

    results = cursor.fetchall()
    return render_template('index.html', results=results)

if __name__ == '__main__':
   # app.run(port=5005)
    socketio.run(app, port=5005, debug=True)