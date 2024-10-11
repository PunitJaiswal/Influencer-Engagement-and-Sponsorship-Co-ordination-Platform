from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin



class Influencer(db.Model, UserMixin):
    __tablename__="Influencer"
    id=db.Column(db.Integer, primary_key=True)
    role=db.Column(db.String, default='Influencer', nullable=False)
    fullname=db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False)
    username=db.Column(db.String, nullable=False, unique=True)
    pwd=db.Column(db.String, nullable=False)
    niche=db.Column(db.String, nullable=False)
    platform=db.Column(db.String, nullable=False)
    followers=db.Column(db.Integer, nullable=False)
    rating=db.Column(db.Float, default=None)
    earning=db.Column(db.Integer, nullable=False, default=0)
    is_flag=db.Column(db.Boolean, nullable=False, default=False)
    # Relationship bw datasets
    ad_request=db.relationship('Ad_request', backref='Influencer')
    Review=db.relationship('Review', backref='Influencer')

class Sponsor(db.Model, UserMixin):
    __tablename__="Sponsor"
    id=db.Column(db.Integer, primary_key=True)
    role=db.Column(db.String, default='Sponsor', nullable=False)
    fullname=db.Column(db.String, nullable=False)
    company_name=db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False)
    username=db.Column(db.String, nullable=False, unique=True)
    pwd=db.Column(db.String, nullable=False)
    is_flag=db.Column(db.Boolean, nullable=False, default=False)
    # Relationship bw datasets
    campaign=db.relationship("Campaign",backref="Sponsor")
    ad_request = db.relationship('Ad_request',backref="Sponsor")
 
class Campaign(db.Model, UserMixin):
    __tablename__='Campaign'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    description=db.Column(db.String, nullable=False)
    start_date=db.Column(db.Date, nullable=False)
    end_date=db.Column(db.Date, nullable=False)
    budget=db.Column(db.Integer, nullable=False)
    visibility=db.Column(db.String, nullable=False)
    niche=db.Column(db.String, nullable=True)
    goals=db.Column(db.String, nullable=False)
    is_flag=db.Column(db.Boolean, nullable=False, default=False)
    # Relationship bw datasets
    sponsor_id=db.Column(db.Integer,db.ForeignKey("Sponsor.id"),nullable=False)
    ad_request = db.relationship('Ad_request', backref="Campaign")
    

class Ad_request(db.Model, UserMixin):
    __tablename__='Ad_request'
    id=db.Column(db.Integer, primary_key=True)
    messages=db.Column(db.String, nullable=False)
    requirements=db.Column(db.String, nullable=True)
    payment_amount=db.Column(db.Integer, nullable=False)
    status=db.Column(db.String, nullable=False,default='Pending')
    completed=db.Column(db.Boolean, default=False)
    payment_done=db.Column(db.Boolean, default=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("Sponsor.id"), nullable=True)
    request_type=db.Column(db.String, nullable=False)
    # Relationship between datasets
    campaign_id=db.Column(db.Integer, db.ForeignKey("Campaign.id"), nullable=False)
    influencer_id=db.Column(db.Integer, db.ForeignKey("Influencer.id"), nullable=False)
    payments = db.relationship('Payment', backref='ad_request')
    

class Payment(db.Model, UserMixin):
    __tablename__ = 'Payment'
    id = db.Column(db.Integer, primary_key=True)
    card_no = db.Column(db.String, nullable=False)
    valid_till = db.Column(db.Date, nullable=False)
    cvv = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    # Relation between tables
    adreq_id = db.Column(db.Integer, db.ForeignKey('Ad_request.id'), nullable=False)


class Review(db.Model, UserMixin):
    __tablename__ = 'Review'
    id=db.Column(db.Integer, primary_key=True)
    review=db.Column(db.String, nullable=False)
    rating=db.Column(db.Integer, nullable=False)
    # Relation between tables
    inf_id=db.Column(db.Integer, db.ForeignKey('Influencer.id'), nullable=False)
    spon_id=db.Column(db.Integer, db.ForeignKey('Sponsor.id'), nullable=False)