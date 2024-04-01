from flask import Flask, render_template, request, session, redirect
import json, re, pymysql, random, string
from datetime import datetime

app = Flask(__name__,static_url_path="/")
app.secret_key = "hello world"

freepass=["d'lock","unlock"]
banned_regid = ["root","admin","user"]

def today_word():
    with open("/var/www/rest/app/static/dictionary data/todaylist", 'r', encoding="utf-8") as f:
        data = f.read()
        if datetime.now().strftime("%Y%m%d") == data.split("\n")[-2].split("|")[0]:
            word = data.split("\n")[-2].split("|")[1]
        else:
            with open("/var/www/rest/app/static/dictionary data/wordlist", 'r') as g:
                wordlist = json.loads(g.read())
            word = random.choice(wordlist)
            with open("/var/www/rest/app/static/dictionary data/todaylist", 'a') as g:
                g.write(datetime.now().strftime("%Y%m%d") + "|" + word + "\n")
    return word

@app.route("/")
def index():
    return render_template("index.html", alpha=string.ascii_uppercase)

@app.route("/Corba")
def corba():
    if request.method=="GET":
        if "logged" in session:
            if session["logged"]: return redirect("/login")
    return render_template("Corba.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if(request.method=="GET"):
        if "logged" not in session: return redirect("/Corba")
        if not session["logged"]: return redirect("/Corba")
        return redirect("/main")
    if "logged" in session:
        if session["logged"]: return json.dumps({"success":False})
    data = request.get_json()
    if("id" not in data.keys() and "pw" not in data.keys()): return json.dumps({"success":False,"error":"NoData"})
    p = re.compile("[^a-zA-Z0-9]")
    if(p.search(data["id"])!=None or p.search(data["pw"])!=None): return json.dumps({"success":False,"error":"SQLFilter"})
    user_id, user_pw = data["id"], data["pw"]

    login_db = pymysql.connect(host="localhost", user="root", password="taebin0408", db="login")
    login_cursor = login_db.cursor(pymysql.cursors.DictCursor)

    print(user_id, user_pw)
    login_cursor.execute("select count(*)=1 as result from login_data where userid='{}' and userpw='{}'".format(user_id, user_pw))
    res = login_cursor.fetchall()[0]["result"]
    if not res: return json.dumps({"success":False, "error":"Login failed..."})
    print("[LOGIN] {} is logged in".format(user_id))
    session["logged"] = True
    session["username"] = user_id
    login_db.close()
    return json.dumps({"success":True})

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method=="GET":
        if "logged" in session:
            if session["logged"]: return redirect("/login")
        return render_template("register.html")
    data = request.get_json()
    print(data)
    if ("id" not in data.keys() and "pw" not in data.keys()): return json.dumps({"success": False, "error": "NoData"})
    p = re.compile("[^a-zA-Z0-9]")
    if (p.search(data["id"]) != None or p.search(data["pw"]) != None): return json.dumps({"success": False, "error": "SQLFilter"})
    user_id, user_pw = data["id"], data["pw"]

    if user_id in banned_regid: return json.dumps({"success":False,"error": "That username is banned"})

    login_db = pymysql.connect(host="localhost", user="root", password="taebin0408", db="login")
    login_cursor = login_db.cursor(pymysql.cursors.DictCursor)

    login_cursor.execute("select count(*)=1 as result from login_data where userid='{}'".format(user_id))
    res = login_cursor.fetchall()[0]["result"]
    if res: return json.dumps({"success":False, "error":"AlreadyAccount"})

    login_cursor.execute("insert into login_data (userid, userpw) values ('{}','{}')".format(user_id, user_pw))
    login_db.commit()
    login_db.close()
    return json.dumps({"success":True})

@app.route("/logout", methods=["POST"])
def logout():
    if "logged" not in session: return json.dumps({"success":False})
    if not session["logged"]: return json.dumps({"success":False})
    del session["logged"]
    del session["username"]
    return json.dumps({"success":True})

@app.route("/main", methods=["GET"])
def mainpg():
    if "logged" not in session: return redirect("/Corba")
    if not session["logged"]: return redirect("/Corba")

    return render_template("main.html", user=session["username"])

@app.route("/chat", methods=["POST"])
def chat():
    if "logged" not in session: return json.dumps({"success":False})
    if not session["logged"]: return json.dumps({"success":False})
    data = request.get_json()
    if "text" not in data: return json.dumps({"success":False})
    user, text = session["username"], data["text"]

    chat_db = pymysql.connect(host="localhost", user="root", password="taebin0408", db="chat")
    chat_cursor = chat_db.cursor(pymysql.cursors.DictCursor)

    chat_cursor.execute("insert into chatlog (userid, chat) values ('{}','{}')".format(user,text))
    chat_db.commit()
    chat_db.close()

    return json.dumps({"success":True})

@app.route("/chatlog")
def chatlog():
    if "logged" not in session: json.dumps({"success":False})
    if not session["logged"]: json.dumps({"success":False})
    chat_db = pymysql.connect(host="localhost", user="root", password="taebin0408", db="chat")
    chat_cursor = chat_db.cursor(pymysql.cursors.DictCursor)
    chat_cursor.execute("select * from chatlog")
    data = chat_cursor.fetchall()

    for idx,i in enumerate(data):
        data[idx]["time"] = i["time"].strftime("%H:%M")
    chat_db.close()
    return json.dumps({"success":True,"text":data})

@app.route("/explain")
def explain():
    if "logged" not in session: return redirect("/Corba")
    if not session["logged"]: return redirect("/Corba")
    return render_template("explain.html")

def _wordle(user, origin):
    user = user.lower()
    origin = origin.lower()
    res = []
    for idx, i in enumerate(user):
        if(origin[idx]==i):
            res.append(2)
        elif(i in origin):
            res.append(1)
        else:
            res.append(0)

    return res

@app.route("/wordle",methods=["POST"])
def wordle():
    if "wordle" not in request.get_json().keys(): return json.dumps({"success":False})
    data = request.get_json()["wordle"]
    with open("/var/www/rest/app/static/dictionary data/wordlist", 'r') as f:
        wordlist = json.loads(f.read())
    data = data.lower()
    if data in freepass: return json.dumps({"success":True,"word":data,"status":[2,2,2,2,2,2]})
    if data not in wordlist: return json.dumps({"success":False,"error":"NoDict"})
    word = today_word()
    return json.dumps({"success":True,"word":data,"status":_wordle(data,word)})

@app.route("/mission1")
def mission():
    if "logged" not in session: return redirect("/Corba")
    if not session["logged"]: return redirect("/Corba")

    return render_template("mission.html",user=session["username"])

@app.route("/mission2")
def mission2():
    if "logged" not in session: return redirect("/Corba")
    if not session["logged"]: return redirect("/Corba")

    return render_template("mission2.html",user=session["username"])

@app.route("/napoli", methods=["POST", "GET"])
def napoli():
    if request.method == "POST":
        if "logged" not in session: return json.dumps({"success":False,"error":"not logged in"})
        if not session["logged"]: return json.dumps({"success":False,"error":"not logged in"})
        data = request.get_json()
        if data["id"] == session["username"]:
            login = pymysql.connect(host="localhost", user="root", password="taebin0408", db="login")
            login_cursor = login.cursor(pymysql.cursors.DictCursor)
            login_cursor.execute(f"update login_data set signed_1=1 where userid=\"{session['username']};\"")
            login.commit()
            return json.dumps({"success":True})
        else: return json.dumps({"success":False,"error":"ID not matched"})
    else:
        if "logged" not in session: return redirect("/Corba")
        if not session["logged"]: return redirect("/Corba")
        login = pymysql.connect(host="localhost", user="root", password="taebin0408", db="login")
        login_cursor = login.cursor(pymysql.cursors.DictCursor)
        login_cursor.execute(f"select * from login_data where userid=\"{session['username']}\";")
        data = login_cursor.fetchall()[0]["signed_1"]
        if not data: return redirect("/Corba")
        return render_template("neapolitan.html",user=session["username"])