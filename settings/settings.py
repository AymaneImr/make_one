from flask import Blueprint, request, url_for, redirect, render_template, session, flash
from admin.models import users
from admin.extensions import db
import random
from email.message import EmailMessage
import ssl
import smtplib

third = Blueprint("third", __name__,template_folder="templates", static_folder="static")

# this page will contain a global user and channel setting 
# 1--> give the user the full controll of his acc 
# 2--> the user can change his 'password' and 'email' and 'username'
# 3--> user have access to delete his acc and his channel 
# 4--> user can make updates in his channel 
# 5--> user can add a phone number to his account

@third.route("/")
def settings():
    return "settings"


@third.route("/change_password", methods=["POST", "GET"])
def change_password():
    if request.method == "POST":
        email_pass = request.form.get("email_ver")
        session["email_pass"] = email_pass
        email_found = users.query.filter_by(email=email_pass).first()
        if email_found:
            def code_generator():
                k = 0
                num_list = []
                for i in range(6):
                    random_num = random.randint(0, 9)
                    num_list.append(random_num)
                    num_list[k] = str(random_num)
                    k += 1
                verification_code = "".join(num_list)
                return verification_code
            def send_code():
                email_sender = "pythonsender02@gmail.com"
                app_password = "omof nqiy kezv czrh"
                email_receiver = session["email_pass"]
                subject = "Verivication code"
                em = EmailMessage()
                em["From"] = email_sender
                em["To"] = email_receiver
                em["Subject"] = subject
                code = code_generator()
                session["veri_code"] = code
                em.set_content(code)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, app_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
            send_code()
            return redirect(url_for("app.verification"))
        else:
            return "email not found"
    else:
        return render_template("password.html")

@third.route("/verification", methods=['POST', 'GET'])
def verification():
    if request.method == "POST":
        code1 = request.form.get("code")
        if code1 == session["veri_code"]:
            return redirect(url_for("app.confirm_pass"))
        else:
            return "<p>bro there's 2 only options,<br><br>either you are somehow blind<br>or<br> you are a damn theif(like what are you gonna achieve if u stole someone's account)</p>"
    else:
        return render_template("verification_code.html")

@third.route("/confirm_pass", methods=["POST", "GET"])
def confirm_pass():
    if request.method == "POST":
        new_pass = request.form.get("new_pass1")
        confirm_pass = request.form.get("new_pass2")
        if new_pass == confirm_pass:
            admin = users.query.filter_by(email=session["email_pass"]).first()
            admin.password = confirm_pass
            db.session.commit()
            return redirect(url_for("app.login"))
        else:
            return "dude come on how old are you, you still can't memorize your new password"
    else:
        return render_template("new_pass.html")


@third.route("/email_verification", methods=["POST", "GET"])
def email_verification():
    if request.method == "POST":
        email = request.form.get("email")
        confirm_email = request.form.get("confirm_email")
        password = request.form.get("password")
        correct_user = users.query.filter_by(username=session["username"]).first()
        correct_email = correct_user.email 
        correct_password = correct_user.password
        if email == correct_email:
            if email == confirm_email:
                if password == correct_password:
                    return redirect(url_for("change_email"))
                else:
                    '''flash -> wrong password Sir'''
                    return ' wrong password Sir'
            else:
                '''flash -> it should be the same email '''
                return 'it should be the same email Sir'
        else:
            '''flash -> this is not your email Sir'''
            return "this is not your email Sir"
    else:
        return render_template("verify_email.html")

@third.route("/change_email", methods=["POST", "GET"])
def change_email():
    if request.method == "POST":
        email = request.form.get("email")
        correct_user = users.query.filter_by(username=session["username"]).first()
        email_exist = users.query.filter(users.email == email).first()
        if not email_exist:
            correct_user.email = email
            db.session.commit()
            return redirect(url_for("settings"))
        else:
            '''flash -> email already taken Sir'''
            return 'email already taken Sir'
    else:
        return render_template("change_email.html")

@third.route("/change-user-info", methods=["POST", "GET"])
def change_user_info():
    if request.method == "POST":
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        username = request.form.get("username")
        password = request.form.get("password")
        correct_user = users.query.filter_by(username=session["username"]).first()
        correct_password = correct_user.password
        username_exist = users.query.filter(users.username == username).first()
        if not username_exist:
            if password == correct_password:
                correct_user.f_name = f_name  
                correct_user.l_name = l_name 
                correct_user.username = username 
                db.session.commit()
                return redirect(url_for("settings"))
            else:
                '''flash -> wrong password Sir'''
                return ' wrong password Sir'
        else:
            '''flash -> username already taken Sir'''
            return ' username already taken Sir'
    else:
        return render_template("user_info.html")


