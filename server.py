from flask import Flask
from config import FLASK_SECRET

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET

@app.route('/authenticate')
def authenticate():
    import tweepy
    from config import CONSUMER_KEY, CONSUMER_SECRET
    from flask import request, redirect, session

    callback_url = request.url.replace( request.endpoint, 'callback' )
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback_url)

    try:
        url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect( url )
    except tweepy.TweepError as e:
        print ( 'Error getting auth URL:', str(e) )
        return maybe_redirect('error=true', 'Error! Failed to get request token.')

@app.route('/callback')
def callback():
    import tweepy
    from config import CONSUMER_KEY, CONSUMER_SECRET
    from flask import request, redirect, session

    if not request.args.get('oauth_token') or not request.args.get('oauth_verifier') or not session.get('request_token'):
        return maybe_redirect( 'error=true', 'Error occurred, please try again.' )

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.request_token = session.get('request_token')

    try:
        auth.get_access_token( verifier=request.args.get('oauth_verifier') )
    except tweepy.TweepError as e:
        print ( 'Error getting access token:', str(e) )
        return maybe_redirect( 'error=true', 'Error occurred, please try again or later, or contact us.' )

    auth.set_access_token(auth.access_token, auth.access_token_secret)
    api = tweepy.API(auth)
    
    try:
        user = api.verify_credentials()

        if hasattr( user, 'id' ) and user.id:
            save_token( user.id, { 'token': auth.access_token, 'secret': auth.access_token_secret } )
        else:
            # failed credentials
            return maybe_redirect( 'error=true', 'Error occurred, please try again or later, or contact us.' )

        return maybe_redirect( 'success=true', 'You are authenticated!' )
    except Exception as e:
        print ( 'Error verifying credentials:', str(e) )
        return maybe_redirect( 'error=true', 'Error occurred, please try again or later, or contact us.' )

def maybe_redirect( query_string='', message='' ):
    from config import REDIRECT_TO as url

    if not url: return message

    if query_string: url += ( '?' if not '?' in url else '&' ) + query_string
    from flask import redirect

    return redirect( url )

def save_token(user_id, obj):
    from config import TOKENS_PATH
    from os.path import isfile 
    from json import load, dump

    if isfile( TOKENS_PATH ):
        with open( TOKENS_PATH ) as f: tokens = load(f)
    else:
        tokens = {}

    tokens[ str(user_id) ] = obj

    with open(TOKENS_PATH, 'w') as f: dump(tokens, f)

if __name__ == "__main__":
    app.run()
