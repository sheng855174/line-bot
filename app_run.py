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
