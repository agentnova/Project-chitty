from flask import Flask, render_template, request, session, jsonify
from dbconnect import Db
import datetime





app = Flask(__name__)

#######################################################################################

@app.route('/')
def lllogin():
    return render_template('login.html')

@app.route('/login', methods=['post'])
def llogin():
    username = request.form['uname']
    password = request.form['upass']
    qry = "select * from login where username='" + username + "' and pass='" + password + "'"
    f = Db()
    res = f.select_one(qry)
    if res is None:
        return "Inavalid details"
    else:
        if res[3] == 'admin':
            return render_template('adm_home.html')
        elif res[3] == 'user':
            session['user_id'] = res[0]
            qw="select name from user where phone='"+password+"'"
            oi=f.select_one(qw)
            return render_template('user_home.html',data=oi)
        else:
            return "Invalid user"

@app.route('/vusers')
def userview():
    qry="select * from user"
    d=Db()
    res=d.select(qry)
    return render_template('view_user.html',data=res)

@app.route('/view_user_history')
def hist():
    qry2 = "SELECT user.NAME FROM USER,login WHERE user.login_id='" + str(session['user_id']) + "' and user.login_id=login.login_id"
    qry = "select chitty.* from chitty,user where user.login_id='" + str(session['user_id']) + "' and user.user_id=chitty.user_id"
    d=Db()
    res = d.select(qry)
    drf = d.select_one(qry2)
    return render_template('chitty_detail.html', data=res, data2=drf)



@app.route('/chitty_details/<uid>')
def details(uid):
    qry2="SELECT NAME FROM USER WHERE user_id='"+uid+"'"
    qry="select chitty.* from chitty,user where chitty.user_id='"+uid+"' and user.user_id=chitty.user_id"
    d=Db()
    res=d.select(qry)
    drf=d.select_one(qry2)
    return render_template('chitty_detail.html',data=res,data2=drf)

@app.route('/user_create_post',methods=['post'])
def usercreatepost():
    c=Db()
    name=request.form['name']
    phone=request.form['phone']
    mail=request.form['email']
    place=request.form['place']
    qry = "select max(login_id) from login"
    log_id = c.mid(qry)
    qry2="insert into user(login_id,name,place,mail,phone) values ('"+str(log_id)+"','"+name+"','"+place+"','"+mail+"','"+phone+"')"
    c.nonreturn(qry2)
    qry3 = "insert into login VALUES('" + str(log_id) + "','" + name + "','" + phone + "','user')"
    c.nonreturn(qry3)
    return render_template('adm_home.html')

@app.route('/updateview')
def updatre():
    qry = "select * from user"
    d = Db()
    res = d.select(qry)
    return render_template('upload.html', data=res)

@app.route('/updatedetaills/<uid>')
def updated(uid):
    qry="select * from user where user_id='"+uid+"'"
    d=Db()
    res=d.select(qry)
    return render_template('updatepage.html',dat=res)


@app.route('/update_post',methods=['post'])
def udarepost():
    status=request.form['status']
    amount=request.form['amount']
    user=request.form['uid']
    x= datetime.datetime.now()
    dt=x.strftime("%x")
    qry="insert into chitty(user_id,amount,status,date) values ('"+user+"','"+amount+"','"+status+"','"+str(dt)+"')"
    d=Db()
    d.nonreturn(qry)
    return render_template('adm_home.html')
@app.route('/createuser')
def usercreate():
    return render_template('user_create.html')





############################################################################################################




if __name__ == '__main__':
    app.run()
