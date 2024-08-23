from flask import Flask, session, redirect, url_for, request, render_template
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
from utils.credentials_to_dict.credentials_to_dict import credentials_to_dict
from utils.dataProcessing.dataProcessing import dataProcessingFilesAll
from utils.databaseUtils.database import setup_db,insert_or_update_file,get_data_files, get_data_history
from dotenv import load_dotenv

app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.secret_key = os.urandom(24)
setup_db()
load_dotenv()

GOOGLE_API_CREDENTIALS = os.getenv('GOOGLE_API_CREDENTIALS')

SCOPES = ['https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid']


@app.route('/')
def index():
    '''Index initial, the user start the application here.'''


    if 'state' not in session:
        return render_template("not_state.html")
    if request.args.get('state') != session['state']:
        return "State mismatch. Possible CSRF attack.", 400
    
    flow = Flow.from_client_secrets_file(
        GOOGLE_API_CREDENTIALS,
        SCOPES,
        state=session['state'],  
        redirect_uri=url_for('index', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('drive'))

@app.route('/login')
def login():
    '''If the user dont have the credentials in the session, she/he must login in the application,'''


    flow = Flow.from_client_secrets_file(
        GOOGLE_API_CREDENTIALS,
        SCOPES,
        redirect_uri=url_for('index', _external=True)
    )

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/drive')
def drive():
    '''Show the data that we have in the database.'''

    
    if 'credentials' not in session:
        return redirect(url_for('login'))

    credentials = Credentials(**session['credentials'])
    service = build('drive', 'v3', credentials=credentials)
    filesProcessing = dataProcessingFilesAll(service)
    insert_or_update_file(filesProcessing)
    files = get_data_files()

    return render_template('index.html', files=files)

@app.route('/history_changes')
def history_changes():
    '''Show the data that we have in the database.'''
    
    files = get_data_history()
    return render_template('history.html', files=files)

if __name__ == "__main__":
    app.run(port=5000)