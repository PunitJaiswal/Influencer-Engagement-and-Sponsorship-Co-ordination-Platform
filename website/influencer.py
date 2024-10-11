from flask import Blueprint, request, render_template, redirect, url_for
from website.models import *
from flask_login import login_required
from .graphs import *

influencer = Blueprint('influencer', __name__)

@influencer.route('/dash_profile/<string:username>', methods=['GET', 'POST'])
@login_required
def dash_profile(username):
        if request.method == 'GET':
            inf = Influencer.query.filter_by(username=username).first()
            adreqs = Ad_request.query.filter_by(influencer_id=inf.id, status='Accepted').all()
            data={}
            for adreq in adreqs:
                camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
                spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
                data[adreq.id] = [camp.name, spon.company_name, camp.end_date, adreq.completed, adreq.payment_done]
            return render_template('/influencer/dash_profile.html', inf=inf, data=data)

@influencer.route('/dash_stats/<int:inf_id>', methods=['GET','POST'])
@login_required
def dash_stats(inf_id):
    adreqs = Ad_request.query.filter_by(influencer_id=inf_id).all()
    inf = Influencer.query.filter_by(id=inf_id).first()
    inf_adreq_status(inf.id)
    adreq_sent_recieved(inf.id)
    payment_recieved(inf.id)
    completed_adreq(inf.id)
    return render_template('/influencer/dash_stats.html', inf=inf, adreqs=adreqs)

@influencer.route('/edit_profile/<int:inf_id>', methods=['GET','POST'])
@login_required
def edit_profile(inf_id):
    inf=Influencer.query.filter_by(id=inf_id).first()
    if request.method=='POST':
        new_fullname=request.form.get('fullname')
        new_email=request.form.get('email')
        new_username=request.form.get('username')
        new_niche=request.form.get('niche')
        new_platform=request.form.get('platform')
        new_followers=request.form.get('followers')

        # Assign new values to the sponsor
        inf.fullname=new_fullname
        inf.email=new_email
        inf.username=new_username
        inf.niche=new_niche
        inf.platform=new_platform
        inf.followers=new_followers
        db.session.commit()
        adreqs = Ad_request.query.filter_by(influencer_id=inf.id, status='Accepted').all()
        data={}
        for adreq in adreqs:
            camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
            spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
            data[adreq.id] = [camp.name, spon.company_name, camp.end_date, adreq.completed, adreq.payment_done]
        return render_template('/influencer/dash_profile.html', inf=inf, data=data)
    return render_template('/influencer/edit_profile.html', inf=inf)

@influencer.route('/dash_find/<int:inf_id>', methods=['GET', 'POST'])
@login_required
def dash_find(inf_id):
        if request.method == 'GET':
            inf=Influencer.query.filter_by(id=inf_id).first()
            camps=Campaign.query.filter_by(visibility='Public',is_flag=False).all()
            private_camps = Campaign.query.filter_by(visibility='Private', niche=inf.niche, is_flag=False).all()
            
            send_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Influencer')
            send_data={}
            for send_req in send_reqs:
                camp = Campaign.query.filter_by(id=send_req.campaign_id).first()
                spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
                send_data[send_req.id] = [camp.name, spon.company_name, send_req.messages, send_req.payment_amount, send_req.status, camp.id]
            recieved_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Sponsor')
            recieved_data={}
            for recieved_req in recieved_reqs:
                camp = Campaign.query.filter_by(id=recieved_req.campaign_id).first()
                spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
                recieved_data[recieved_req.id] = [camp.name, spon.company_name, recieved_req.requirements, recieved_req.payment_amount, recieved_req.status, camp.id]
            return render_template('/influencer/dash_find.html', inf=inf, camps=camps, private_camps=private_camps, send_data=send_data, recieved_data=recieved_data)

@influencer.route('/<int:inf_id>/view_campaign/<int:camp_id>', methods=['GET','POST'])
@login_required
def view_campaign(inf_id,camp_id):
    if request.method=='GET':
        camp = Campaign.query.filter_by(id=camp_id).first()
        inf = Influencer.query.filter_by(id=inf_id).first()
        return render_template('/influencer/view_campaign.html', inf=inf, camp=camp)


@influencer.route('/accept_request/<int:adreq_id>', methods=['GET','POST'])
@login_required
def accept_request(adreq_id):
    adreq = Ad_request.query.filter_by(id=adreq_id).first()
    adreq.status='Accepted'
    db.session.commit()
    inf=Influencer.query.filter_by(id=adreq.influencer_id).first()
    camps=Campaign.query.filter_by(visibility='Public')
    send_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Influencer')
    send_data={}
    for send_req in send_reqs:
        camp = Campaign.query.filter_by(id=send_req.campaign_id).first()
        spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
        send_data[send_req.id] = [camp.name, spon.company_name, send_req.messages, send_req.payment_amount, send_req.status, camp.id]
    recieved_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Sponsor')
    recieved_data={}
    for recieved_req in recieved_reqs:
        camp = Campaign.query.filter_by(id=recieved_req.campaign_id).first()
        spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
        recieved_data[recieved_req.id] = [camp.name, spon.company_name, recieved_req.requirements, recieved_req.payment_amount, recieved_req.status, camp.id]
    return render_template('/influencer/dash_find.html', inf=inf, camps=camps, send_reqs=send_reqs, send_data=send_data, recieved_reqs=recieved_reqs, recieved_data=recieved_data)


@influencer.route('/reject_request/<int:adreq_id>', methods=['GET','POST'])
@login_required
def reject_request(adreq_id):
    adreq = Ad_request.query.filter_by(id=adreq_id).first()
    adreq.status='Rejected'
    db.session.commit()
    inf=Influencer.query.filter_by(id=adreq.influencer_id).first()
    send_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Influencer')
    send_data={}
    for send_req in send_reqs:
        camp = Campaign.query.filter_by(id=send_req.campaign_id).first()
        spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
        send_data[send_req.id] = [camp.name, spon.company_name, send_req.messages, send_req.payment_amount, send_req.status, camp.id]
    recieved_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Sponsor')
    recieved_data={}
    for recieved_req in recieved_reqs:
        camp = Campaign.query.filter_by(id=recieved_req.campaign_id).first()
        spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
        recieved_data[recieved_req.id] = [camp.name, spon.company_name, recieved_req.requirements, recieved_req.payment_amount, recieved_req.status, camp.id]
    return render_template('/influencer/dash_find.html', inf=inf, send_reqs=send_reqs, send_data=send_data, recieved_reqs=recieved_reqs, recieved_data=recieved_data)


@influencer.route('/mark_completed/<int:adreq_id>', methods=['GET','POST'])
@login_required
def mark_completed(adreq_id):
    adreq = Ad_request.query.filter_by(id=adreq_id).first()
    adreq.completed=True
    db.session.commit()
    inf = Influencer.query.filter_by(id=adreq.influencer_id).first()
    adreqs = Ad_request.query.filter_by(influencer_id=inf.id, status='Accepted').all()
    data={}
    for adreq in adreqs:
        camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
        spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
        data[adreq.id] = [camp.name, spon.company_name, camp.end_date, adreq.completed, adreq.payment_done]
    return render_template('/influencer/dash_profile.html', inf=inf, data=data)


@influencer.route('/<int:inf_id>/create_campaign_request/<int:camp_id>',  methods=['GET','POST'])
@login_required
def create_campaign_request(inf_id,camp_id):
    inf = Influencer.query.filter_by(id=inf_id).first()
    camp = Campaign.query.filter_by(id=camp_id).first()
    spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
    if request.method == 'POST':
        message = request.form.get('message')
        payment_amount = request.form.get('payment_amount')
        
        new_ad_request = Ad_request.query.filter_by(campaign_id=camp.id).first()
        if not new_ad_request:
            new_ad_request = Ad_request(campaign_id=camp.id, messages=message, payment_amount=payment_amount, influencer_id=inf_id, sponsor_id=spon.id, request_type='Influencer')
            db.session.add(new_ad_request)
            db.session.commit()

            inf=Influencer.query.filter_by(id=inf_id).first()
            camps=Campaign.query.filter_by(is_flag=False, visibility='Public').all()
            send_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Influencer')
            send_data={}
            for send_req in send_reqs:
                camp = Campaign.query.filter_by(id=send_req.campaign_id).first()
                spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
                send_data[send_req.id] = [camp.name, spon.company_name, send_req.messages, send_req.payment_amount, send_req.status, camp.id]
            recieved_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Sponsor')
            recieved_data={}
            for recieved_req in recieved_reqs:
                camp = Campaign.query.filter_by(id=recieved_req.campaign_id).first()
                spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
                recieved_data[recieved_req.id] = [camp.name, spon.company_name, recieved_req.requirements, recieved_req.payment_amount, recieved_req.status, camp.id]
            return render_template('/influencer/dash_find.html', inf=inf, camps=camps, send_reqs=send_reqs, send_data=send_data, recieved_reqs=recieved_reqs, recieved_data=recieved_data)
        else:
            return render_template('/influencer/create_campaign_request.html',camp=camp, inf=inf, msg='Ad request already sent')
    
    return render_template('/influencer/create_campaign_request.html', camp=camp, inf=inf)



@influencer.route('/<int:inf_id>/search_campaign', methods=['GET','POST'])
@login_required
def search_campaign(inf_id):
    inf = Influencer.query.filter_by(id=inf_id).first()
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            camps = Campaign.query.filter(Campaign.name.like("%"+name+"%")).all()

            send_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Influencer')
            send_data={}
            for send_req in send_reqs:
                camp = Campaign.query.filter_by(id=send_req.campaign_id).first()
                spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
                send_data[send_req.id] = [camp.name, spon.company_name, send_req.messages, send_req.payment_amount, send_req.status, send_req.completed, send_req.payment_done, camp.id]
            recieved_reqs = Ad_request.query.filter_by(influencer_id=inf.id, request_type='Sponsor')
            recieved_data={}
            for recieved_req in recieved_reqs:
                camp = Campaign.query.filter_by(id=recieved_req.campaign_id).first()
                spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
                recieved_data[recieved_req.id] = [camp.name, spon.company_name, recieved_req.requirements, recieved_req.payment_amount, recieved_req.status, recieved_req.completed, recieved_req.payment_done, camp.id]
            return render_template('/influencer/dash_find.html', inf=inf, camps=camps, send_reqs=send_reqs, send_data=send_data, recieved_reqs=recieved_reqs, recieved_data=recieved_data)