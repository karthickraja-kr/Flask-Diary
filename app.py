from flask import Flask, render_template, redirect, request, url_for, session
import pyrebase


config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": ""
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

app = Flask(__name__)
# Home page
app.secret_key = ""


@app.route("/")
def index():
    return render_template("index.html")

# About page

@app.route("/about.html")
def about():
    return render_template("about.html")

#login page

@app.route("/login.html" , methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        user = auth.sign_in_with_email_and_password(email, password)
        a = auth.get_account_info(user['idToken'])
        b = a["users"][0]["localId"]
        session["email"] = b
        try:
            auth.sign_in_with_email_and_password(email, password)
            return redirect("/appcontent.html")

        except:
            return render_template("login.html", message="Wrong Credentials" )  
    return render_template("login.html")

#sign up page

@app.route("/signup.html" , methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        verify = "Please Check your Inbox to verify your email"
        email = request.form['email']
        password = request.form['pass']
        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect("/login.html")
        except:
            return render_template("signup.html", message="The email is already taken, try another one, please" )
    return render_template("signup.html")    


#app contents

@app.route("/appcontent.html",methods = ['GET','POST'])
def appcontent():
    if "email" in session:
        email = session["email"]
        if request.method == "POST":
            title = request.form["title"]
            message = request.form["message"]
            name = {
                "title": title,
                "message": message
            }
            db.child("diary").child(email).push(name)
            todo = db.child("diary").child(email).get()
            va = todo.val()
            return render_template("/appcontent.html",t=va.values())

        todo = db.child("todo").child(email).get()
        va = todo.val()
        if va == None:
            return render_template("/appcontent.html")
        else:
            return render_template("/appcontent.html",t=va.values())
    else:
        return redirect(url_for("login"))



#logout route
@app.route("/logout.html")
def logout():
    session.clear()
    return redirect("/")
    
# main 

if __name__ == "__main__":
    app.run(debug=True)

