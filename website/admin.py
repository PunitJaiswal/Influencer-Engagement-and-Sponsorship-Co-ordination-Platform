from flask import Blueprint, request, render_template, redirect, url_for
from website.models import *
from flask_login import login_required, current_user
from .graphs import *

admin = Blueprint('admin', __name__)

@admin.route("/dash_info", methods=['GET','POST'])
def dash_info():
    if request.method=='GET':
        counts = count_data()
        # generate data for graphs
        category_count()
        influencer_niche_count()
        influencer_flagged()
        sponsor_flagged()
        campaign_flagged()
        
        return render_template('/admin/dash_info.html', counts=counts)
    
@admin.route('/dash_find', methods=['GET','POST'])
def dash_find():
    if request.method=='GET':
        infs=Influencer.query.all()
        spons=Sponsor.query.all()
        camps=Campaign.query.all()
        return render_template('/admin/dash_find.html', infs = infs, spons = spons, camps = camps)
    
@admin.route('/view_campaign/<int:camp_id>', methods = ['GET', 'POST'])
def view_campaign(camp_id):
    if request.method == 'GET':
        camp=Campaign.query.filter_by(id=camp_id).first()
        return render_template('/admin/view_campaign.html', camp=camp)
    
@admin.route('/view_influencer/<int:inf_id>', methods = ['GET', 'POST'])
def view_influencer(inf_id):
    if request.method == 'GET':
        inf = Influencer.query.filter_by(id = inf_id).first()
        return render_template('/admin/view_influencer.html', inf = inf)
    
@admin.route('/view_sponsor/<int:spon_id>', methods = ['GET', 'POST'])
def view_sponsor(spon_id):
    if request.method == 'GET':
        spon = Sponsor.query.filter_by(id = spon_id).first()
        return render_template('/admin/view_sponsor.html', spon = spon)
    

@admin.route('/view_ad_request', methods=['GET','POST'])
def view_Ad_request():
    adreqs = Ad_request.query.all()
    return render_template('/admin/view_ad_request.html', adreqs = adreqs)

@admin.route('/flag_campaign/<int:camp_id>', methods=['GET','POST'])
def flag_campaign(camp_id):
    camp=Campaign.query.filter_by(id=camp_id).first()
    if camp.is_flag==False:
        camp.is_flag=True
    else:
        camp.is_flag=False
    db.session.commit()
    infs=Influencer.query.all()
    spons=Sponsor.query.all()
    camps=Campaign.query.all()
    return render_template('/admin/dash_find.html', infs = infs, spons = spons, camps = camps)

@admin.route('/flag_influencer/<int:inf_id>', methods=['GET','POST'])
def flag_influencer(inf_id):
    inf=Influencer.query.filter_by(id=inf_id).first()
    if inf.is_flag==False:
        inf.is_flag=True
    else:
        inf.is_flag=False
    db.session.commit()
    infs=Influencer.query.all()
    spons=Sponsor.query.all()
    camps=Campaign.query.all()
    return render_template('/admin/dash_find.html', infs = infs, spons = spons, camps = camps)

@admin.route('/flag_sponsor/<int:spon_id>', methods=['GET','POST'])
def flag_sponsor(spon_id):
    spon=Sponsor.query.filter_by(id=spon_id).first()
    if spon.is_flag==False:
        spon.is_flag=True
    else:
        spon.is_flag=False
    db.session.commit()
    infs=Influencer.query.all()
    spons=Sponsor.query.all()
    camps=Campaign.query.all()
    return render_template('/admin/dash_find.html', infs = infs, spons = spons, camps = camps)



# Some important Functions
def count_data():
    inf_count = Influencer.query.count()
    spon_count = Sponsor.query.count()
    camp_count = Campaign.query.count()
    adreq_count = Ad_request.query.count()
    counts=[inf_count, spon_count, camp_count, adreq_count]
    return counts
