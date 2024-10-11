from flask import Blueprint, request, render_template, redirect, url_for, flash
from .models import *
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .graphs import *


auth = Blueprint('auth', __name__)

@auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        uname = request.form.get("uname")
        pwd = request.form.get('pwd')
        if uname == "admin" and pwd == "12345":
            category_count()
            influencer_niche_count()
            influencer_flagged()
            sponsor_flagged()
            campaign_flagged()
            counts=count_data()
            return render_template('/admin/dash_info.html', counts=counts)
    return render_template('admin_login.html')

@auth.route("/user_login", methods=['GET','POST'])
def user_login():
    if request.method=="POST":
        role=request.form.get('role')
        uname=request.form.get('uname')
        pwd=request.form.get('pwd')
        inf=Influencer.query.filter_by(username=uname,role=role, is_flag=False).first()
        spon=Sponsor.query.filter_by(username=uname, role=role, is_flag=False).first()
        if inf:
            if check_password_hash(inf.pwd, pwd):
                login_user(inf)
                adreqs = Ad_request.query.filter_by(influencer_id=inf.id, status='Accepted').all()
                data={}
                for adreq in adreqs:
                    camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
                    spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
                    data[adreq.id] = [camp.name, spon.company_name, camp.end_date, adreq.completed, adreq.payment_done]
                return render_template('/influencer/dash_profile.html', inf=inf, data=data)
            else:
                return render_template("user_login.html", msg='Username or password doesn\'t match')
        elif spon:
            if check_password_hash(spon.pwd, pwd):
                login_user(spon)
                adreqs = Ad_request.query.filter_by(sponsor_id=spon.id, status='Accepted').all()
                data={}
                for adreq in adreqs:
                    camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
                    inf = Influencer.query.filter_by(id=adreq.influencer_id).first()
                    data[adreq.id] = [camp.name, inf.fullname, adreq.payment_amount, adreq.completed, adreq.payment_done, inf.id]
                return render_template('/sponsor/dash_profile.html', spon=spon, data=data)
            else:
                return render_template("user_login.html", msg='Username or password doesn\'t match')
        else:
            return render_template("user_login.html", msg='Username or password doesn\'t match')

    return render_template("user_login.html",msg='')

@auth.route("/influencer_registration", methods=['GET','POST'])
def influencer_registration():
    if request.method=='POST':
        fullname=request.form.get('fullname')
        username=request.form.get('username')
        pwd=request.form.get('pwd')
        email=request.form.get('email')
        niche=request.form.get('niche')
        platform=request.form.get('platform')
        followers=request.form.get('followers')

        # generate password hash
        pwd=generate_password_hash(pwd)
        usr=Influencer.query.filter_by(username=username).first()
        if not usr:
            new_user=Influencer(fullname=fullname, username=username, pwd=pwd, niche=niche, platform=platform, email=email, followers=followers)
            db.session.add(new_user)
            db.session.commit()
            return render_template('user_login.html', msg="User Registered!")
        else:
            return render_template('influencer_registration.html', msg="User is already registered!")
    return render_template("influencer_registration.html")

@auth.route("/sponsor_registration", methods=['GET','POST'])
def sponsor_registration():
    if request.method=='POST':
        fullname=request.form.get('fullname')
        email=request.form.get('email')
        username=request.form.get('username')
        pwd=request.form.get('pwd')
        company_name=request.form.get('company_name')
        usr=Sponsor.query.filter_by(username=username).first()
        # generate password hash
        pwd = generate_password_hash(pwd)
        if not usr:
            new_user=Sponsor(fullname=fullname, username=username, pwd=pwd, email=email, company_name=company_name)
            db.session.add(new_user)
            db.session.commit()
            return render_template('user_login.html', msg="User Registered!")
        else:
            return render_template('sponsor_registration.html', msg="User is already registered!")
    return render_template("sponsor_registration.html")



@auth.route('/admin_logout')
def admin_logout():
    logout_user()
    return render_template('admin_login.html')

@auth.route('/user_logout')
def user_logout():
    logout_user()
    return render_template('user_login.html')


    


# Some important functions
def fetch_campaigns(spon_id):
    camps=Campaign.query.filter_by(sponsor_id=spon_id).all()
    return camps


def count_data():
    inf_count = Influencer.query.count()
    spon_count = Sponsor.query.count()
    camp_count = Campaign.query.count()
    adreq_count = Ad_request.query.count()
    counts=[inf_count, spon_count, camp_count, adreq_count]
    return counts