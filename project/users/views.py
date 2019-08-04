import sys
import time
import requests
import datetime
from project import db
from datetime import timedelta
# from project.users.models import Users, Counter
from project.users.request_acceptor import InstagramBot
from flask_login import login_required, login_user, logout_user, current_user
from flask import Blueprint, render_template, redirect, url_for, request, session
import memcache


sys.path.append('../../')


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/request_accepted_counter', methods=['GET', 'POST'])
def request_accepted_counter():
    try:
        if Counter:
            counterval = Counter.query.filter_by(insta_username=session['insta_username']).first()
    except:
        time.sleep(0.10)
        ctr = "0"
    # except sqlite3.OperationalError as e:
    #     print('[-] Sqlite operational error: {} Retrying...'.format(e))
    #     ctr = "0"
    # except sqlite3.InterfaceError as e:
    #     print('[-] Sqlite interface error: {} Retrying...'.format(e))
    #     ctr = "0"
    # except sqlite3.Error:
    #     # time.sleep(0.10)
    #     ctr = "0"  # str(session["request_accepted_counter_demo"])

    if counterval is not None:
        ctr = str(counterval.counts)

    counterval = None
    client = memcache.Client([('127.0.0.1', 11211)])
    ctr = client.get(session['insta_username'])

    if ctr == None:
        ctr = "0"
    print("counter: ", ctr)
    return ctr


@login_required
@users_blueprint.route('/accept_pending_requests', methods=['GET', 'POST'])
def accept_pending_requests():

    if request.method == 'POST':
        resp = 'Success'
        custom_number = request.form['customUserInputNumber']
        try:
            custom_number = int(custom_number)
        except:
            custom_number = int(custom_number[:-1])

        insta_obj = InstagramBot(
            session['insta_username'],
            session['insta_password'])
        insta_obj.login2()
        counts = insta_obj.pending_request_count()

        instagram_accept_request_count = custom_number

        try:
            if counts <= instagram_accept_request_count:
                insta_obj.accept_pending_requests(counts)
            else:
                insta_obj.accept_pending_requests(instagram_accept_request_count)
        except:
            resp = "No request to accept"

        return resp, 200

    try:
        user = Users.query.filter_by(
            insta_username=session['insta_username']).first()
        till_date = user.till_date
        last_day = (till_date - datetime.datetime.utcnow()).days

    except BaseException:
        last_day = None

    countval = Counter.query.filter_by(insta_username=session['insta_username']).first()

    if countval is None:
        newcounts = Counter(insta_username=session['insta_username'])
        db.session.add(newcounts)
        db.session.commit()
        countval = Counter.query.filter_by(insta_username=session['insta_username']).first()

    countval.counts = 0
    db.session.commit()

    return render_template(
        'AcceptRequests.html', instagram_username=session['insta_username'], last_day=last_day)


@users_blueprint.route('/request_accepted_count/<int:num>', methods=['GET', 'POST'])
def request_accepted_count(num):
    counter = Counter.query.filter_by(insta_username=session['insta_username']).first()
    client = memcache.Client([('127.0.0.1', 11211)])
    ctr = client.get(session['insta_username'])
    
    # if counter is not None:
    #    ctr = counter.counts 

    return render_template('request_accepted_count.html', num=ctr)


@users_blueprint.route('/live_counter', methods=['GET', 'POST'])
def live_counter():

    if request.method == 'POST':
        try:

            instagram_username = request.form['instagram_username']
            session['live_counter'] = instagram_username
            response = requests.get(
                'https://www.instagram.com/web/search/topsearch/?query={un}'.format(un=instagram_username))
            resp = response.json()
            for i in resp['users']:
                if i['user']['username'] == instagram_username.lower():
                    count = i['user']['follower_count']
            name = '@' + \
                instagram_username[0].capitalize() + instagram_username[1:]
            return render_template('count_display.html',
                                   name=name, user_count=count)
        except BaseException:
            return render_template('LiveCounter.html')
    return render_template('LiveCounter.html')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        instagram_username = request.form['userEmailID']
        instagram_password = request.form['userLoginPassword']

        session['insta_username'] = instagram_username
        session['insta_password'] = instagram_password
        session['request_accepted_counter_demo'] = 0
        insta_bot = InstagramBot(instagram_username, instagram_password)
        insta_login_response = insta_bot.login()
        insta_bot.closeBrowser()

        if insta_login_response == False:
            msg = 'Invalid Credentails'
            return render_template('index.html', msg=msg)

        if insta_login_response:
            user_obj = Users.query.filter_by(
                insta_username=instagram_username).first()
            if not user_obj:
                new_user = Users(insta_username=instagram_username)
                db.session.add(new_user)
                db.session.commit()

        user = Users.query.filter_by(insta_username=instagram_username).first()
        if insta_login_response and user is not None:
            user.is_subscribed = True
            user.till_date = datetime.datetime.utcnow() + timedelta(days=1)
            if user.is_subscribed:
                if datetime.datetime.utcnow() < user.till_date:
                    ok = login_user(user)
                    next = request.args.get('next')

                    if next is None or not next[0] == '/':
                        next = url_for('users.accept_pending_requests')
                    return redirect(next)

            if user.is_subscribed == False:
                try:
                    if datetime.datetime.utcnow() > user.till_date:
                        user.till_date = None
                        user.from_date = None
                        user.is_subscribed = False
                        db.session.commit()
                except BaseException:
                    ok = login_user(user)
                    next = request.args.get('next')
                    if next is None or not next[0] == '/':
                        next = url_for('core.pricing')
                    return redirect(next)

        client = memcache.Client([('12.0.0.1', 11211)])
        client.set(instagram_username, 0)
    return render_template('index.html')


@login_required
@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))
