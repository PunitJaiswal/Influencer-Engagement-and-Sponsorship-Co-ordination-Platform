from .models import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import base64

matplotlib.use('Agg')

def format_pct_and_count(pct, allvals):
    absolute = int(pct / 100. * sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)


# ----------Graphs for Admin Portal ------------------------
def category_count():
    # Query counts directly from the database
    inf_count = Influencer.query.count()
    spon_count = Sponsor.query.count()
    camp_count = Campaign.query.count()
    adreq_count = Ad_request.query.count()
    if inf_count and spon_count and camp_count and adreq_count:
        # Create bar chart
        categories = ['Influencers', 'Sponsors', 'Campaigns', 'Ad Requests']
        counts = [inf_count, spon_count, camp_count, adreq_count]

        plt.bar(categories, counts, color=['blue', 'green', 'orange', 'red'], align='center', alpha=0.5)
        plt.xticks(categories, ['Influencer','Sponsor','Campaign','Ad Requests'])  # Rotate x-axis labels if necessary
        plt.xlabel('User Types')
        plt.ylabel('Count')
        plt.title('Counts of Different Entities')

        file_path = 'website/static/images/category_count.png'
        plt.savefig(file_path)
        plt.close()
        return file_path

def influencer_niche_count():
    infs = Influencer.query.all()
    if infs:
        tech_count, fitness_count, travel_count, lifestyle_count, finance_count =0, 0, 0, 0, 0
        for inf in infs:
            if inf.niche == 'Tech':
                tech_count += 1
            if inf.niche == 'Fitness':
                fitness_count += 1
            if inf.niche == 'Travel':
                travel_count += 1
            if inf.niche == 'Lifestyle':
                lifestyle_count += 1
            if inf.niche == 'Finance':
                finance_count += 1

        niche = ['Tech',  'Fitness', 'Travel', 'Lifestyle', 'Finance']
        counts=[tech_count, fitness_count, travel_count,  lifestyle_count, finance_count]

        plt.bar(niche, counts, color=['blue', 'green', 'orange', 'red', 'yellow'], align='center', alpha=0.5)
        plt.xlabel('Different Niche')
        plt.ylabel('Count')
        plt.title('Counts of Influencers in different niche')

        plt.savefig('website/static/images/influencer_niche_count.png')
        plt.close()
        return 'website/static/images/influencer_niche_count.png'

def influencer_flagged():
    infs = Influencer.query.all()
    if infs:
        if infs:
            flagged = 0
            not_flagged = 0
            for inf in infs:
                if inf.is_flag == True:
                    flagged +=1
                else:
                    not_flagged +=1
            labels = ['Flagged', 'NOT Flagged']
            sizes = [flagged, not_flagged]
            plt.title('Influencers Flagged Vs Not Flagged')
            colors = ['red', 'yellowgreen']
            explode = (0.1, 1)
            plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
            plt.axis('equal')
            plt.savefig('website/static/images/influencer_flagged.png')
            plt.close()
            return 'website/stataic/images/influencer_flagged.png'

def sponsor_flagged():
    spons = Sponsor.query.all()
    if spons:
        if spons:
            flagged = 0
            not_flagged = 0
            for spon in spons:
                if spon.is_flag == True:
                    flagged +=1
                else:
                    not_flagged +=1
            labels = ['Flagged', 'NOT Flagged']
            sizes = [flagged, not_flagged]
            plt.title('Sponsors Flagged Vs Not Flagged')
            colors = ['red', 'yellowgreen']
            explode = (0.1, 1)
            plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
            plt.axis('equal')
            plt.savefig('website/static/images/sponsor_flagged.png')
            plt.close()
            return 'website/stataic/images/sponsor_flagged.png'

def campaign_flagged():
    camps = Campaign.query.all()
    if camps:
        flagged = 0
        not_flagged = 0
        for camp in camps:
            if camp.is_flag == True:
                flagged +=1
            else:
                not_flagged +=1
        labels = ['Flagged', 'NOT Flagged']
        sizes = [flagged, not_flagged]
        plt.title('Campaigns Flagged Vs Not Flagged')
        colors = ['red', 'yellowgreen']
        explode = (0.1, 1)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
        plt.axis('equal')
        plt.savefig('website/static/images/campaign_flagged.png')
        plt.close()
        return 'website/stataic/images/campaign_flagged.png'

    
# ------------------Graphs for Influencer Portal------------------------
def inf_adreq_status(inf_id):
    adreqs = Ad_request.query.filter_by(influencer_id=inf_id).all()
    if adreqs:
        pending = 0
        accepted = 0
        rejected = 0

        for adreq in adreqs:
            if adreq.status == 'Pending' or adreq.status=='pending':
                pending+=1
            if adreq.status == 'Accepted':
                accepted+=1
            if adreq.status == 'Rejected':
                rejected+=1

        labels =['Pending', 'Accepted', 'Rejected']
        sizes = [pending, accepted, rejected]
        plt.title('Ad Request Status')
        colors=['orange', 'green', 'red']
        explode=(0.1,0,0)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct,sizes), shadow=True, startangle=140)
        plt.axis('equal')
        plt.savefig('website/static/images/inf_adreq_status.png')
        plt.close()
        return 'website/static/images/inf_adreq_status.png'

def adreq_sent_recieved(inf_id):
    adreqs = Ad_request.query.filter_by(influencer_id=inf_id).all()
    if adreqs:
        sent_request = 0
        recieved_request = 0
        for adreq in adreqs:
            if adreq.request_type=='Influencer':
                sent_request += 1
            else:
                recieved_request += 1
        labels = ['Send Requests', 'Recieved Requests']
        sizes = [sent_request, recieved_request]
        plt.title('Ad Request (Sent VS Recieved)')
        colors = ['orange', 'yellowgreen']
        explode = (0.1,1)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
        plt.axis('equal')
        plt.savefig('website/static/images/adreq_sent_recieved.png')
        plt.close()
        return 'website/stataic/images/adreq_sent_recieved.png'

def payment_recieved(inf_id):
    inf = Influencer.query.filter_by(id=inf_id).first()
    adreqs = Ad_request.query.filter_by(influencer_id=inf.id).all()
    if adreqs:
        payments = []
        camps = []
        for adreq in adreqs:
            camp = Campaign.query.filter_by(id=adreq.campaign_id).first()
            camps.append(camp.name)
            if adreq.payment_done:
                payments.append(adreq.payment_amount)
            else:
                payments.append(0)

        plt.bar(camps, payments, color=['blue', 'green', 'orange', 'red', 'yellow'], align='center', alpha=0.5)
        plt.xlabel('Campaign Name')
        plt.ylabel('Payments Recieved')
        plt.title('Payment Recieved from Campaigns')

        plt.savefig('website/static/images/payment_recieved.png')
        plt.close()
        return 'website/static/images/payment_recieved.png'

def completed_adreq(inf_id):
    inf = Influencer.query.filter_by(id=inf_id).first()
    adreqs = Ad_request.query.filter_by(influencer_id=inf.id).all()
    if adreqs:
        completed, not_completed = 0,0
        for adreq in adreqs:
            if adreq.completed:
                completed += 1
            else:
                not_completed += 1

        labels = ['Completed', 'Not Completed']
        sizes = [completed, not_completed]
        plt.title('Campaigns Completed VS not completed')
        colors = ['yellowgreen', 'red']
        explode = (0.1, 1)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
        plt.axis('equal')
        plt.savefig('website/static/images/completed_adreq.png')
        plt.close()
        return 'website/stataic/images/completed_adreq.png'


# ----------------Graphs for Sponsor Portal----------------------

def spon_adreq_sent_recieved(spon_id):
    adreqs = Ad_request.query.filter_by(sponsor_id=spon_id).all()
    if adreqs:
        sent_request = 0
        recieved_request = 0
        for adreq in adreqs:
            if adreq.request_type=='Sponsor':
                sent_request += 1
            else:
                recieved_request += 1
        labels = ['Send Requests', 'Recieved Requests']
        sizes = [sent_request, recieved_request]
        plt.title('Ad Request (Sent VS Recieved)')
        colors = ['orange', 'yellowgreen']
        explode = (0.1,1)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
        plt.axis('equal')
        plt.savefig('website/static/images/spon_adreq_sent_recieved.png')
        plt.close()
        return 'website/stataic/images/spon_adreq_sent_recieved.png'

def payment_done(spon_id):
    spon=Sponsor.query.filter_by(id=spon_id).first()
    adreqs = Ad_request.query.filter_by(sponsor_id=spon.id).all()
    if adreqs:
        payment_done = 0
        payment_not_done=0
        for adreq in adreqs:
            if adreq.payment_done:
                payment_done += 1
            else:
                payment_not_done += 1
        x_pos =['Payment Done', 'Payment Not Done']
        y_pos = [payment_done, payment_not_done]
        plt.bar(x_pos, y_pos, color=['yellowgreen', 'orange'], align='center', alpha=0.5)
        plt.xlabel('Payment Status')
        plt.ylabel('Count')
        plt.title('Payment for Campaign done or not')

        plt.savefig('website/static/images/payment_done.png')
        plt.close()
        return 'website/static/images/payment_done.png'

def spon_adreq_status(spon_id):
    spon = Sponsor.query.filter_by(id=spon_id).first()
    adreqs = Ad_request.query.filter_by(sponsor_id=spon_id).all()
    if adreqs:
        pending = 0
        accepted = 0
        rejected = 0

        for adreq in adreqs:
            if adreq.status == 'Pending':
                pending+=1
            if adreq.status == 'Accepted':
                accepted+=1
            if adreq.status == 'Rejected':
                rejected+=1

        labels =['Pending', 'Accepted', 'Rejected']
        sizes = [pending, accepted, rejected]
        plt.title('Sponsor Ad Request Status')
        colors=['orange', 'green', 'red']
        explode=(0.1,0,0)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct,sizes), shadow=True, startangle=140)
        plt.axis('equal')
        plt.savefig('website/static/images/spon_adreq_status.png')
        plt.close()
        return 'website/static/images/spon_adreq_status.png'