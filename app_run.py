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
        history_dic['SmartPhone'] = _data.SmartPhone
        history_dic['Time'] = _data.Time
        history_dic['Description'] = _data.Description
        history_list.append(history_dic)
        history_dic = {}
    return render_template('index.html', **locals())


@app.route('/API/add_data', methods=['POST'])
def add_data():
    id = request.form['Id']
    level = request.form['Level']
    name = request.form['Name']
    smartPhone = request.form['SmartPhone']
    time = request.form['Time']
    description = request.form['Description']
    if name != "" and description != "":
        add_data = UserData(
            Id=id,
            Level=level,
            Name=name,
            SmartPhone=smartPhone,
            Time=time,
            Description=description,
        )
        db.session.add(add_data)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
