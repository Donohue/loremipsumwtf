import sys
import os
import requests
from mailchimp import Mailchimp, Lists
from flask import Flask, flash, render_template, redirect, request

if not 'APP_SECRET_KEY' in os.environ:
    print 'Missing secret key'
    sys.exit(-1)
elif not 'MAILCHIMP_API_KEY' in os.environ:
    print 'Missing MailChimp API key'
    sys.exit(-1)
elif not 'MAILCHIMP_LIST_ID' in os.environ:
    print 'Missing MailChimp list ID'
    sys.exit(-1)

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.environ['APP_SECRET_KEY']

MAILCHIMP_API_KEY = os.environ['MAILCHIMP_API_KEY']
MAILCHIMP_LIST_ID = os.environ['MAILCHIMP_LIST_ID']
mailchimp = Mailchimp(MAILCHIMP_API_KEY)
mailchimp_list = Lists(mailchimp)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/landing/logan_lee_date_10_2015/index.html')
def landing():
    return render_template('landing.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    name = request.form.get('name')
    email = request.form.get('email')

    name_parts = name.split(' ')
    if len(name_parts) < 2:
        flash('Last name too, please. Or just make something up.', 'error')
        return redirect('/')

    fname = name_parts[0]
    lname = name_parts[1]
    try:
        mailchimp_list.subscribe(MAILCHIMP_LIST_ID, {'email': email}, {'FNAME': fname, 'LNAME': lname}, double_optin=False)
        flash('great choice. see you in your inbox.', 'success')
    except Exception, e:
        print 'Error: %s' % e
        flash('Ooh something went wrong. Fucking internet. Try again in a second.', 'error')
    return redirect('/')

