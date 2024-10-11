from flask import Blueprint, request, render_template, redirect, url_for
from .models import *
from flask_login import login_required
from datetime import datetime
from .graphs import *

sponsor = Blueprint('sponsor', __name__)

@sponsor.route('/dash_profile/<string:username>', methods=['GET','POST'])
@login_required
def dash_profile(username):
    if request.method == 'GET':
        spon = Sponsor.query.filter_by(username=username).first()
        adreqs = Ad_request.query.filter_by(sponsor_id=spon.id, status='Accepted').all()
        data={}
        for adreq in adreqs:
            camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
            inf = Influencer.query.filter_by(id=adreq.influencer_id).first()
            data[adreq.id] = [camp.name, inf.fullname, adreq.payment_amount, adreq.completed, adreq.payment_done, inf.id]
        return render_template('/sponsor/dash_profile.html', spon=spon, data=data)

@sponsor.route('/dash_stats/<int:spon_id>',methods=['GET',"POST"])
@login_required
def dash_stats(spon_id):
    adreqs = Ad_request.query.filter_by(sponsor_id=spon_id).all()
    spon = Sponsor.query.filter_by(id=spon_id).first()
    spon_adreq_sent_recieved(spon.id)
    spon_adreq_status(spon.id)
    payment_done(spon.id)
    return render_template('/sponsor/dash_stats.html',adreqs=adreqs, spon=spon)
    
@sponsor.route('/edit_profile/<int:spon_id>', methods=['GET','POST'])
@login_required
def edit_profile(spon_id):
    spon=Sponsor.query.filter_by(id=spon_id).first()
    if request.method=='POST':
        new_fullname=request.form.get('fullname')
        new_email=request.form.get('email')
        new_username=request.form.get('username')
        new_company_name=request.form.get('company_name')

        # Assign new values to the sponsor
        spon.fullname=new_fullname
        spon.email=new_email
        spon.username=new_username
        spon.company_name=new_company_name
        db.session.commit()
        adreqs = Ad_request.query.filter_by(sponsor_id=spon.id, status='Accepted').all()
        data={}
        for adreq in adreqs:
            camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
            inf = Influencer.query.filter_by(id=adreq.influencer_id).first()
            data[adreq.id] = [camp.name, inf.fullname, adreq.payment_amount, adreq.completed, adreq.payment_done, inf.id]
        return render_template('/sponsor/dash_profile.html', spon=spon, data=data)
    return render_template('/sponsor/edit_profile.html', spon=spon)

@sponsor.route('/dash_campaign/<int:spon_id>', methods=['GET','POST'])
@login_required
def dash_campaign(spon_id):
    if request.method == 'GET':
        spon=Sponsor.query.filter_by(id=spon_id).first()
        camps=fetch_campaigns(spon_id)

        send_reqs = Ad_request.query.filter_by(sponsor_id=spon.id, request_type='Sponsor').all()
        recieved_reqs = Ad_request.query.filter_by(sponsor_id=spon_id, request_type='Influencer').all()
        send_data={}
        for send_req in send_reqs:
            camp=Campaign.query.filter_by(id=send_req.campaign_id).first()
            inf = Influencer.query.filter_by(id=send_req.influencer_id).first()
            send_data[send_req.id]=[camp.name, inf.fullname, send_req.payment_amount, send_req.status]
        
        recieved_data={}
        for recieved_req in recieved_reqs:
            camp=Campaign.query.filter_by(id=recieved_req.campaign_id).first()
            inf=Influencer.query.filter_by(id=recieved_req.influencer_id).first()
            recieved_data[recieved_req.id] = [camp.name, inf.fullname, recieved_req.payment_amount, recieved_req.status, recieved_req.messages]
        return render_template('/sponsor/dash_campaign.html', spon=spon, camps=camps, send_reqs=send_reqs, recieved_reqs=recieved_reqs, send_data=send_data, recieved_data=recieved_data)

@sponsor.route('/dash_find/<int:spon_id>', methods=['GET','POST'])
@login_required
def dash_find(spon_id):
    if request.method == 'GET':
        infs=Influencer.query.all()
        spon=Sponsor.query.filter_by(id=spon_id).first()
        return render_template('/sponsor/dash_find.html', infs=infs, spon=spon)


@sponsor.route("/add_campaign/<int:spon_id>",methods=["GET","POST"])
@login_required
def add_campaign(spon_id):
    spon=Sponsor.query.filter_by(id=spon_id).first()
    if request.method=='POST':
        camp_name=request.form.get('camp_name')
        description=request.form.get('description')
        start_date=request.form.get('start_date')
        end_date=request.form.get('end_date')
        budget=request.form.get('budget')
        visibility=request.form.get('visibility')
        niche=request.form.get('niche')
        goals=request.form.get('goals')
        # convert date string to datetime object
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Fetch campaigns
        camp=Campaign.query.filter_by(name=camp_name).first()
        if not camp:
            if visibility=='Private':
                new_camp = Campaign(name=camp_name, description=description, start_date=start_date, end_date=end_date, budget=budget, visibility=visibility, goals=goals, sponsor_id=spon_id, niche=niche)
            else:
                new_camp=Campaign(name=camp_name, description=description, start_date=start_date, end_date=end_date, budget=budget, visibility=visibility, goals=goals, sponsor_id=spon_id)
            db.session.add(new_camp)
            db.session.commit()
            camps = fetch_campaigns(spon_id)
            send_reqs = Ad_request.query.filter_by(sponsor_id=spon.id, request_type='Sponsor').all()
            recieved_reqs = Ad_request.query.filter_by(sponsor_id=spon_id, request_type='Influencer').all()
            send_data={}
            for send_req in send_reqs:
                camp=Campaign.query.filter_by(id=send_req.campaign_id).first()
                inf = Influencer.query.filter_by(id=send_req.influencer_id).first()
                send_data[send_req.id]=[camp.name, inf.fullname, send_req.payment_amount, send_req.status]

            recieved_data={}
            for recieved_req in recieved_reqs:
                camp=Campaign.query.filter_by(id=recieved_req.campaign_id).first()
                inf=Influencer.query.filter_by(id=recieved_req.influencer_id).first()
                recieved_data[recieved_req.id] = [camp.name, inf.fullname, recieved_req.payment_amount, recieved_req.status, recieved_req.messages]
            return render_template('/sponsor/dash_campaign.html', spon=spon, camps=camps, send_data=send_data, recieved_data=recieved_data)
        else:
            return render_template('/sponsor/add_campaign.html', spon=spon, msg='Campaign is already registered.')
    return render_template('/sponsor/add_campaign.html', spon=spon)

@sponsor.route("/view_campaign/<int:camp_id>", methods=['GET','POST'])
@login_required
def view_campaign(camp_id):
    if request.method == 'GET':
        camp = Campaign.query.filter_by(id=camp_id).first()
        spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
        return render_template('/sponsor/view_campaign.html', camp=camp, spon=spon)

@sponsor.route('/edit_campaign/<int:camp_id>',methods=['GET','POST'])
def edit_campaign(camp_id):
    camp=Campaign.query.filter_by(id=camp_id).first()
    spon=Sponsor.query.filter_by(id=camp.sponsor_id).first()
    if request.method=='POST':
        new_camp_name=request.form.get('camp_name')
        new_description=request.form.get('description')
        new_start_date=request.form.get('start_date')
        new_end_date=request.form.get('end_date')
        new_budget=request.form.get('budget')
        new_visibility=request.form.get('visibility')
        new_niche=request.form.get('niche')
        new_goals=request.form.get('goals')
        # convert date string to datetime object
        new_start_date = datetime.strptime(new_start_date, '%Y-%m-%d').date()
        new_end_date = datetime.strptime(new_end_date, '%Y-%m-%d').date()

        # Assign new values to campaign
        camp.name=new_camp_name
        camp.description=new_description
        camp.start_date=new_start_date
        camp.end_date=new_end_date
        camp.budget=new_budget
        camp.visibility=new_visibility
        camp.niche=new_niche
        camp.goals=new_goals
        db.session.commit()
        camps = fetch_campaigns(spon.id)

        send_reqs = Ad_request.query.filter_by(sponsor_id=spon.id, request_type='Sponsor').all()
        recieved_reqs = Ad_request.query.filter_by(sponsor_id=spon.id, request_type='Influencer').all()
        send_data={}
        for send_req in send_reqs:
            camp=Campaign.query.filter_by(id=send_req.campaign_id).first()
            inf = Influencer.query.filter_by(id=send_req.influencer_id).first()
            send_data[send_req.id]=[camp.name, inf.fullname, send_req.payment_amount, send_req.status]
        
        recieved_data={}
        for recieved_req in recieved_reqs:
            camp=Campaign.query.filter_by(id=recieved_req.campaign_id).first()
            inf=Influencer.query.filter_by(id=recieved_req.influencer_id).first()
            recieved_data[recieved_req.id] = [camp.name, inf.fullname, recieved_req.payment_amount, recieved_req.status, recieved_req.messages]
        return render_template('/sponsor/dash_campaign.html', spon=spon, camps=camps, send_data=send_data, recieved_data=recieved_data)

    return render_template('/sponsor/edit_campaign.html', camp=camp)
    
@sponsor.route("/delete_campaign/<int:camp_id>",methods=["POST",'GET'])
@login_required
def delete_campaign(camp_id):
    if request.method=='GET':
        camp=Campaign.query.filter_by(id=camp_id).first()
        db.session.delete(camp)
        db.session.commit()
        spon=Sponsor.query.filter_by(id=camp.sponsor_id).first()
        camps=fetch_campaigns(spon.id)

        send_reqs = Ad_request.query.filter_by(sponsor_id=spon.id, request_type='Sponsor').all()
        recieved_reqs = Ad_request.query.filter_by(sponsor_id=spon.id, request_type='Influencer').all()
        send_data={}
        for send_req in send_reqs:
            camp=Campaign.query.filter_by(id=send_req.campaign_id).first()
            inf = Influencer.query.filter_by(id=send_req.influencer_id).first()
            send_data[send_req.id]=[camp.name, inf.fullname, send_req.payment_amount, send_req.status]
        
        recieved_data={}
        for recieved_req in recieved_reqs:
            camp=Campaign.query.filter_by(id=recieved_req.campaign_id).first()
            inf=Influencer.query.filter_by(id=recieved_req.influencer_id).first()
            recieved_data[recieved_req.id] = [camp.name, inf.fullname, recieved_req.payment_amount, recieved_req.status, recieved_req.messages]
        return render_template('/sponsor/dash_campaign.html', spon=spon, camps=camps, send_reqs=send_reqs, recieved_reqs=recieved_reqs, send_data=send_data, recieved_data=recieved_data)



@sponsor.route('/<int:spon_id>/view_influencer/<int:inf_id>', methods=['GET','POST'])
@login_required
def view_influencer(spon_id, inf_id):
    inf = Influencer.query.filter_by(id=inf_id).first()
    spon= Sponsor.query.filter_by(id=spon_id).first()
    return render_template('/sponsor/view_influencer.html', inf= inf, spon=spon)


@sponsor.route('/<int:spon_id>/create_request/<int:inf_id>', methods=['GET', 'POST'])
@login_required
def create_request(inf_id, spon_id):
    camps = Campaign.query.filter_by(sponsor_id=spon_id).all()
    inf = Influencer.query.get(inf_id)
    spon = Sponsor.query.filter_by(id=spon_id).first()
    
    if request.method == 'POST':
        camp_name = request.form.get('select_campaign')
        message = request.form.get('message')
        payment_amount = request.form.get('payment_amount')
        requirements = request.form.get('requirements')
        
        camp = Campaign.query.filter_by(name=camp_name).first()
        
        ad_request = Ad_request.query.filter_by(campaign_id=camp.id, influencer_id=inf_id).first()
        if not ad_request:
            new_ad_request = Ad_request(campaign_id=camp.id, sponsor_id=spon_id, messages=message, payment_amount=payment_amount, influencer_id=inf_id, requirements=requirements, request_type='Sponsor')
            db.session.add(new_ad_request)
            db.session.commit()
            spon = Sponsor.query.get(camp.sponsor_id)  # Corrected to use .get() for primary key lookup
            infs = Influencer.query.all()
            return render_template('/sponsor/dash_find.html', infs=infs, spon=spon, msg='Request Created!')
        else:
            return render_template('/sponsor/ad_request.html', camps=camps, inf=inf, spon=spon, msg='Ad request already sent')
    
    return render_template('/sponsor/create_request.html', camps=camps,spon=spon, inf=inf)


@sponsor.route('/make_payment/<int:adreq_id>', methods=['GET','POST'])
@login_required
def make_payment(adreq_id):
    adreq = Ad_request.query.filter_by(id=adreq_id).first()
    inf = Influencer.query.filter_by(id=adreq.influencer_id).first()
    camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
    spon = Sponsor.query.filter_by(id=camp.sponsor_id).first()
    camps = Campaign.query.filter_by(sponsor_id=spon.id).all()
    adreqs = Ad_request.query.all()
    if request.method=='POST':
        card_no = request.form.get('card_no')
        valid_till = request.form.get('valid_till')
        cvv = request.form.get('cvv')
        payment_amount = request.form.get('payment_amount')

        valid_till = datetime.strptime(valid_till, '%Y-%m-%d').date()
        # Fetch payment
        payment=Payment.query.filter_by(adreq_id=adreq_id).first()
        if not payment:
            new_payment=Payment(card_no=card_no, valid_till=valid_till, cvv=cvv, payment_amount=payment_amount, adreq_id=adreq_id)
            db.session.add(new_payment)
            inf.earning += int(payment_amount)
            adreq.payment_done=True
            db.session.commit()
            adreqs = Ad_request.query.filter_by(sponsor_id=spon.id, status='Accepted').all()
            data={}
            for adreq in adreqs:
                camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
                inf = Influencer.query.filter_by(id=adreq.influencer_id).first()
                data[adreq.id] = [camp.name, inf.fullname, adreq.payment_amount, adreq.completed, adreq.payment_done, inf.id]
            return render_template('/sponsor/dash_profile.html', spon=spon, data=data)
        else:
            return render_template('/sponsor/make_payment.html', adreq=adreq, msg='Already Done Payment')
    return render_template('/sponsor/make_payment.html', adreq=adreq)

@sponsor.route('/<int:spon_id>/review_influencer/<int:inf_id>', methods=['GET','POST'])
def review_influencer(inf_id, spon_id):
    inf=Influencer.query.filter_by(id=inf_id).first()
    spon=Sponsor.query.filter_by(id=spon_id).first()
    if request.method=='POST':
        review=request.form.get('review')
        rating=request.form.get('rating')
        new_review=Review.query.filter_by(inf_id=inf_id, spon_id=spon_id).first()
        if not new_review:
            new_review=Review(review=review, rating=rating, spon_id=spon_id, inf_id=inf_id)
            db.session.add(new_review)
            if inf.rating is None:
                inf.rating = float(rating)
            else:
                inf.rating = (inf.rating + float(rating)) / 2
            db.session.commit()

            adreqs = Ad_request.query.filter_by(sponsor_id=spon.id, status='Accepted').all()
            data={}
            for adreq in adreqs:
                camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
                inf = Influencer.query.filter_by(id=adreq.influencer_id).first()
                data[adreq.id] = [camp.name, inf.fullname, adreq.payment_amount, adreq.completed, adreq.payment_done, inf.id]
            return render_template('/sponsor/dash_profile.html', spon=spon, data=data)
        return render_template('/sponsor/review_influencer.html', inf=inf, spon=spon, msg='Review is already submitted')
    else:
        return render_template('/sponsor/review_influencer.html', inf=inf, spon=spon, msg='')

# Ad request Actions

@sponsor.route('/<int:spon_id>/accept_request/<int:adreq_id>', methods=['GET','POST'])
def accept_request(adreq_id, spon_id):
    adreq = Ad_request.query.filter_by(id=adreq_id).first()
    spon = Sponsor.query.filter_by(id=spon_id).first()
    adreq.status='Accepted'
    db.session.commit()
    spon=Sponsor.query.filter_by(id=spon_id).first()
    camps=fetch_campaigns(spon_id)
    send_reqs = Ad_request.query.filter_by(sponsor_id=spon.id, request_type='Sponsor').all()
    recieved_reqs = Ad_request.query.filter_by(sponsor_id=spon_id, request_type='Influencer').all()
    send_data={}
    for send_req in send_reqs:
        camp=Campaign.query.filter_by(id=send_req.campaign_id).first()
        inf = Influencer.query.filter_by(id=send_req.influencer_id).first()
        send_data[send_req.id]=[camp.name, inf.fullname, send_req.payment_amount, send_req.status]
    recieved_data={}
    for recieved_req in recieved_reqs:
        camp=Campaign.query.filter_by(id=recieved_req.campaign_id).first()
        inf=Influencer.query.filter_by(id=recieved_req.influencer_id).first()
        recieved_data[recieved_req.id] = [camp.name, inf.fullname, recieved_req.payment_amount, recieved_req.status, recieved_req.messages]
    return render_template('/sponsor/dash_campaign.html', spon=spon, camps=camps, send_data=send_data, recieved_data=recieved_data)


@sponsor.route('/<int:spon_id>/reject_request/<int:adreq_id>', methods=['GET','POST'])
def reject_request(adreq_id,spon_id):
    adreq = Ad_request.query.filter_by(id=adreq_id).first()
    spon = Sponsor.query.filter_by(id=spon_id).first()
    adreq.status='Rejected'
    db.session.commit()
    spon=Sponsor.query.filter_by(id=spon_id).first()
    camps=fetch_campaigns(spon_id)
    send_reqs = Ad_request.query.filter_by(sponsor_id=spon.id, request_type='Sponsor').all()
    recieved_reqs = Ad_request.query.filter_by(sponsor_id=spon_id, request_type='Influencer').all()
    send_data={}
    for send_req in send_reqs:
        camp=Campaign.query.filter_by(id=send_req.campaign_id).first()
        inf = Influencer.query.filter_by(id=send_req.influencer_id).first()
        send_data[send_req.id]=[camp.name, inf.fullname, send_req.payment_amount, send_req.status]
    
    recieved_data={}
    for recieved_req in recieved_reqs:
        camp=Campaign.query.filter_by(id=recieved_req.campaign_id).first()
        inf=Influencer.query.filter_by(id=recieved_req.influencer_id).first()
        recieved_data[recieved_req.id] = [camp.name, inf.fullname, recieved_req.payment_amount, recieved_req.status, recieved_req.messages]
    return render_template('/sponsor/dash_campaign.html', spon=spon, camps=camps, send_data=send_data, recieved_data=recieved_data)
        

@sponsor.route('/<int:spon_id>/search_influencer', methods=['GET','POST'])
def search_influencer(spon_id):
    spon = Sponsor.query.filter_by(id=spon_id).first()
    infs = Influencer.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        niche = request.form.get('niche')
        followers = request.form.get('followers')
        if name:
            if niche:
                if followers:
                    infs = Influencer.query.filter(Influencer.fullname.like("%"+name+"%"), Influencer.niche.like("%"+niche+"%"), Influencer.followers>int(followers)).all()
                infs = Influencer.query.filter(Influencer.fullname.like("%"+name+"%"), Influencer.niche.like("%"+niche+"%")).all()
            infs = Influencer.query.filter(Influencer.fullname.like("%"+name+"%")).all()
        elif niche:
            if name:
                if followers:
                    infs = Influencer.query.filter(Influencer.fullname.like("%"+name+"%"), Influencer.niche.like("%"+niche+"%"), Influencer.followers>int(followers)).all()
                infs = Influencer.query.filter(Influencer.fullname.like("%"+name+"%"), Influencer.niche.like("%"+niche+"%")).all()
            infs = Influencer.query.filter(Influencer.niche.like("%"+niche+"%")).all()
        elif followers:
            if name:
                if niche:
                    infs = Influencer.query.filter(Influencer.fullname.like("%"+name+"%"), Influencer.niche.like("%"+niche+"%"), Influencer.followers>int(followers)).all()
                infs = Influencer.query.filter(Influencer.followers>int(followers), Influencer.name.like("%"+name+"%")).all() 
            infs = Influencer.query.filter(Influencer.followers>int(followers)).all()
        return render_template('/sponsor/dash_find.html', infs=infs, spon=spon)
    return render_template('/sponsor/dash_find.html', infs=infs, spon=spon)






# Some important Functions
def fetch_campaigns(spon_id):
    camps=Campaign.query.filter_by(sponsor_id=spon_id).all()
    return camps