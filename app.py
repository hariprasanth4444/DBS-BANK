from flask import Flask, render_template, request
import mysql.connector as mysql

app=Flask(__name__)
app.secret_key='Hari4444'

db = mysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database='db'
)

cursor = db.cursor()

@app.route('/')
def sample():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admin')
def admin_log():
    return render_template('admin_login.html')

@app.route('/admin_page')
def admin_page():
    return render_template('admin.html')

@app.route('/admin_login',methods=['POST'])
def admin():
    r = request.form['mobi']
    p = request.form['psw']
    result = getDataFromAdmin(r,p)
    if result:
        cursor.execute('SELECT * FROM DATA')
        result = cursor.fetchall()
        data = []
        for i in result:
            data.append(i)
        return render_template('admin.html',res = data)
    else:
        return render_template('admin_login.html',res = 'Invalid Credentials')

@app.route('/admin_data')
def admin_data1():
    cursor.execute(" SELECT * FROM DATA ")
    result = cursor.fetchall()
    db.commit()
    data = []
    for i in result:
        data.append(i)
    return render_template('admin.html',res = data)
        

def getDataFromAdmin(mob,psw):
    cursor.execute("SELECT * FROM ADMIN_DB WHERE mobile = %s AND password = %s",(mob,psw))
    result = cursor.fetchone()
    return result

@app.route('/coll_admin',methods=['POST'])
def check():
    mobnum = request.form['mob']
    date = request.form['time']
    sql = 'SELECT * FROM DATA WHERE mobile = %s'
    val = (mobnum,)
    cursor.execute(sql,val)
    result = cursor.fetchone()
    if result:
        sql = "UPDATE data SET datetime = %s WHERE mobile = %s"
        val = (date,mobnum)
        cursor.execute(sql,val)
        db.commit()
        return render_template("admin.html",res1 = "Data Updated")
    else:
        return render_template("admin.html",res1 = "Invalid Number")

@app.route('/collect',methods=['POST']) #Collect the data(Handler)  
def collectData():
    n = request.form['name']
    m = request.form['mob']
    dt = request.form['acnt']
    k=getdetails(n,m)
    if k:
        sql = 'UPDATE DATA SET STATUS = NULL, DATETIME = NULL WHERE name = %s'

        val = (n,)
        cursor.execute(sql,val)
        db.commit()
        return render_template('register.html',res = (n+" "+"Request Sent"))
    else:
        storedata(n,m,dt)
        r = "Data Request Sent"
        return render_template('register.html',res=r)

@app.route('/collectcheck',methods=['POST'])
def checkstatus():
    mobnum = request.form['mob']
    # print(mobnum)
    sql = 'SELECT * FROM DATA WHERE mobile = %s'
    val = (mobnum,)
    cursor.execute(sql,val)
    result =  cursor.fetchone()
    if result:
        print(result)
        if result[3]== None:
            return render_template('status.html',res1 = "Decision Pending")
        else:
            dt = str(result[4])
            d = dt[8:10]+"-"+dt[5:8]+dt[:4]
            t = dt[11:]
            dt = d+" "+t
            return render_template('status.html',res1 = "Approved",res2 = 'at', res3 = dt)
    else:
        return render_template("login.html",res='Invalid Credentials')

@app.route('/collectmob',methods=['POST']) #Collect the data(Handler)  
def collectmob():
        m = request.form['mob']
        st = request.form['status']
        # print(st)
        sql = 'SELECT * FROM DATA WHERE mobile = %s'
        val = (m,)
        cursor.execute(sql,val)
        result =  cursor.fetchone()
        if result[3] != None:
            if st == 'approve':
                k = 'Approved'
                sql = "UPDATE DATA SET status = %s WHERE mobile = %s"
                val = (k,m)
                cursor.execute(sql,val)
                db.commit()
                return render_template('status.html',res1=k)
            elif st == 'reject':
                kn = 'Rejected'
                sql = "UPDATE DATA SET status = %s WHERE MOBILE = %s"
                val = (kn,m)
                cursor.execute(sql,val)
                db.commit()
                return render_template('status.html',res1=kn)
            elif st == "assign":
                dt = request.form['time']
                k = 'Approved'
                sql = "UPDATE DATA SET status = %s WHERE mobile = %s"
                val = (k,m)
                cursor.execute(sql,val)
                db.commit()
                sql = "UPDATE DATA SET datetime  = %s WHERE MOBILE = %s"
                val = (dt,m)
                cursor.execute(sql,val)
                db.commit()
                dt = str(dt)
                d = dt[8:10]+"-"+dt[5:8]+dt[:4]
                t = dt[11:]
                dt = d+" "+t
                return render_template('status.html',res1 = k,res2 = "at", res3 = dt)
        else:
            return render_template('status.html',res1 = "Still the Decision is pending")

def getdetails(name,mob):
    cursor.execute("SELECT * FROM DATA WHERE name = %s AND mobile = %s",(name,mob))
    result=cursor.fetchone()
    return result

def storedata(name,mob,account): #Private function not a handler
    sql = "INSERT INTO DATA (name,mobile,ACC_NUM) VALUES (%s,%s,%s)"
    val = (name,mob,account)
    cursor.execute(sql,val)
    db.commit()

if __name__=="__main__":
    app.run(debug=True)