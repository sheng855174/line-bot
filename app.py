from flask import Flask, request, abort
import time
from dbModel import *
import psycopg2

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('E8M/Zgv4jKfyH/13Y/qcZ3YosAzkp9IRUFDRN0ZOYvKUVFLBrjqCAQzKruz6y2dvODQ57vf07Y+DlJJ4CZCHzToyhLm8dhPkmcz4aFNwFicKuHnDl2WGeNTA9id2jRVhr4Mhr2RyoP39f+7Wonbl0gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6af8e930dab9b3a977719185adc48a99')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
    text += "display_name ： " + profile.display_name + "\n"
    text += "user_id ： " + profile.user_id + "\n"
    text += "type ： " + event.source.type + "\n"
    '''
    if event.source.type == "group":
        group_id = event.source.group_id
        text += "group_id ： " + group_id + "\n\n"
        if group_id == "C193ba92879d441b6a12a533a18be62a9":
            if (event.message.text == "!print") or (event.message.text == "！print"):
                data_UserData = UserData.query.all()
                for _data in data_UserData:
                    text += str(_data.Id) + ", "
                    text += str(_data.Level) + ", "
                    text += str(_data.Name) + ", "
                    text += str(_data.Phone) + "\n"
                    text += str(_data.Time) + ", "
                    text += str(_data.Description)
                    text += "\n\n"
            if (event.message.text.find("!query") != -1) or (event.message.text.find("！query") != -1):
                id = event.message.text.split(' ')[1]
                try:
                    connection = psycopg2.connect(database="d9858nlbmqmtfl", user="jmwsmzobgczcti", password="17582fad1e5b57cf0bd0a2530040657bc30d00ce5ae90ea99d2e46ae04357406", host="ec2-174-129-27-158.compute-1.amazonaws.com", port="5432")
                    cursor  = connection.cursor()
                    postgreSQL_select_Query = "select * from \"UserData\" where \"Id\"=%s"
                    cursor.execute(postgreSQL_select_Query, (id,))
                    result = cursor.fetchall()
                    for row in result:
                        text += str(row[0]) + ", "
                        text += row[1] + ", "
                        text += row[2] + ", "
                        text += row[3] + "\n"
                        text += row[4] + ", "
                        text += row[5] + "\n\n"
                except(Exception, psycopg2.Error) as error :
                    print ("Error while fetching data from PostgreSQL", error)
                finally:
                    #closing database connection.
                    if(connection):
                        cursor.close()
                        connection.close()
                        print("PostgreSQL connection is closed")
            if (event.message.text.find("!update") != -1) or (event.message.text.find("！update") != -1):
                id = event.message.text.split(' ')[1]
                description = event.message.text.split(' ')[2]
                try:
                    connection = psycopg2.connect(database="d9858nlbmqmtfl", user="jmwsmzobgczcti", password="17582fad1e5b57cf0bd0a2530040657bc30d00ce5ae90ea99d2e46ae04357406", host="ec2-174-129-27-158.compute-1.amazonaws.com", port="5432")
                    cursor  = connection.cursor()
                    sql_update_query = "Update \"UserData\" set \"Description\"=%s where \"Id\"=%s"
                    cursor.execute(sql_update_query, (description, id))
                    connection.commit()
                    
                    postgreSQL_select_Query = "select * from \"UserData\" where \"Id\"=%s"
                    cursor.execute(postgreSQL_select_Query, (id,))
                    result = cursor.fetchall()
                    for row in result:
                        text += str(row[0]) + ", "
                        text += row[1] + ", "
                        text += row[2] + ", "
                        text += row[3] + "\n"
                        text += row[4] + ", "
                        text += row[5] + "\n\n"
                except(Exception, psycopg2.Error) as error :
                    print ("Error while fetching data from PostgreSQL", error)
                finally:
                    #closing database connection.
                    if(connection):
                        cursor.close()
                        connection.close()
                        print("PostgreSQL connection is closed")
    print(text)
    message = TextSendMessage(text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
'''
from flask import *
from datetime import datetime
from dbModel import *

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    data = "Deploying a Flask App To Heroku"
    data_UserData = UserData.query.all()
    history_dic = {}
    history_list = []
    for _data in data_UserData:
        history_dic['Id'] = _data.Id
        history_dic['Level'] = _data.Level
        history_dic['Name'] = _data.Name
        history_dic['Phone'] = _data.Phone
        history_dic['Time'] = _data.Time
        history_dic['Description'] = _data.Description
        history_list.append(history_dic)
        history_dic = {}
        print("query data")
        print(history_list)
    return render_template('index.html', **locals())


@app.route('/API/add_data', methods=['POST'])
def add_data():
    id = int(request.form['id'])
    level = request.form['level']
    name = request.form['name']
    phone = request.form['phone']
    time = request.form['time']
    description = request.form['description']
    if id != "":
        add_data = UserData(
            Id=id,
            Level=level,
            Name=name,
            Phone=phone,
            Time=time,
            Description=description
        )
        print("add data")
        print(add_data)
        db.session.add(add_data)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

'''
