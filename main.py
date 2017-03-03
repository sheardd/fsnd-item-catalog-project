from flask import (Flask, render_template, request, redirect, jsonify,
                        url_for, flash)
from sqlalchemy import create_engine, asc, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Artist, Album, Track
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# debug start

import logging

logging.basicConfig(filename='log_filename.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# debug end

app = Flask(__name__)

# Establish client secrets for Google+

CLIENT_ID = json.loads(
    open('/var/www/html/itemcatalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "MiTunes"

# Connect to Database and create database session

engine = create_engine('postgresql+psycopg2://catalog:udacity@localhost/mitunes')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token and direct to the login page


@app.route('/login')
def showLogin():
    logging.debug('showLogin called')
    if 'username' in login_session:
        return redirect(url_for('showArtists'))
    else:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        logging.debug(state)
        login_session['state'] = state
        logging.debug('login_session:')
        logging.debug(login_session)
        return render_template('login.html', STATE=state)

# Handles authentication via Facebook - checks login state to verify that the
# user is the one contacting the server, then accesses app credentials in
# fb_secrets.json, which are then submitted along with the given short-life
# token. When this has been exchanged for a long-life token, it then requests
# user info from the facebook API, which it then assigns to login_session along
# with the access token. If a user with the retrieved email address does not
# exist, it creates one. Finally, it responds to the browser with an html
# string containing a welcome message, which will trigger a timeout for the
# browser to redirect to the home page.


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(
                        open('fb_client_secrets.json', 'r')
                        .read())['web']['app_id']
    app_secret = json.loads(
                            open('fb_client_secrets.json', 'r')
                            .read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?'
    url += 'grant_type=fb_exchange_token&client_id=%s'
    url += '&client_secret=%s&fb_exchange_token=%s'
    result = http2GETRequest(url, 1, app_id, app_secret, access_token)

    # Use token to get user info from API

    userinfo_url = "https://graph.facebook.com/v2.4/me"

    # strip expire tag from access token

    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email'
    result = http2GETRequest(url, 1, token)
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # Strip the expires tag out of the token string

    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture

    url = 'https://graph.facebook.com/v2.4/me/picture?%s'
    url += '&redirect=0&height=200&width=200'
    result = http2GETRequest(url, 1, token)
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = renderOutput(login_session)
    return output

# Handles authentication via G+; very similar to the above function,
# with a few extra steps. Again, verifies the user's state, before
# exchanging the user's code for an access token. It then checks that the acess
# token is valid and meant for both our user and our app. It finally checks
# that our user is not already logged in, before requesting and assiging user
# info using Google+'s API, creating a new user if need be. Finally, it renders
# the same output message as before using login_session and returns it to the
# browser to assert that login was successful before redirecting.


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        json_response = json.dumps('Invalid state parameter.')
        response = make_response(json_response, 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        json_response = json.dumps('Failed to upgrade authorization code.')
        response = make_response(json_response, 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
    result = http2GETRequest(url, 1, access_token)
    result = json.loads(result)

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        json_response = json.dumps("Token's user ID doesn't match user ID.")
        response = make_response(json_response, 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        json_response = json.dumps("Token's client ID does not match app's.")
        response = make_response(json_response, 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if (stored_access_token is not None) and (gplus_id == stored_gplus_id):
        json_response = json.dumps("Current user is already connected.")
        response = make_response(json_response, 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = renderOutput(login_session)
    return output

# Called by /disconnect to handle a facebook logout. Fetches the user's
# facebook id and access_token, and submits a DELETE request to facebook to
# clear the session


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token=%s' %
           (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return

# Called by /disconnect to handle a google+ logout. Fetches the user's
# g+ id and access_token, and submits a GET request to google to
# clear the session.


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'
    result = http2GETRequest(url, 0, access_token)
    return

# Determines the provider in login_session, calls the respective function
# to clear the session depending on provider and delete provider-specific info,
# then deletes all common data in login_session.


@app.route('/logout')
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have been logged out.")
        return redirect(url_for('showArtists'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showArtists'))

# --- All JSON API endpoints --- #

# JSON API to view all Artists


@app.route('/artists/JSON/')
def showArtistsJSON():
    artists = getAllArtists()
    return jsonify(Artists=[a.serialize for a in artists])

# JSON API to view an Artist's Discography


@app.route('/artists/<int:artist_id>/discography/JSON/')
def showDiscographyJSON(artist_id):
    albums = getDiscography(artist_id)
    if albums:
        return jsonify(Discography=[a.serialize for a in albums])
    else:
        return invalidJSON()

# JSON API to view an Album's Tracklisting with track info

ALBUM_URL = '/artists/<int:artist_id>/discography/<int:album_id>'
@app.route(ALBUM_URL + '/tracklisting/JSON/')
def showTracklistJSON(artist_id, album_id):
    tracks = getTracklisting(artist_id, album_id)
    if tracks:
        return jsonify(Tracklisting=[t.serialize for t in tracks])
    else:
        return invalidJSON()

# JSON API to view a single Artist


@app.route('/artists/<int:artist_id>/JSON/')
def singleArtistJSON(artist_id):
    artist = getArtist(artist_id)
    if artist:
        return jsonify(Artist=[artist.serialize])
    else:
        return invalidJSON()

# JSON API to view a single Album's general info


@app.route(ALBUM_URL + '/JSON/')
def singleAlbumJSON(artist_id, album_id):
    album = getAlbumInfo(artist_id, album_id)
    if album:
        return jsonify(Album=[album.serialize])
    else:
        return invalidJSON()

# JSON API to view a single track


@app.route(ALBUM_URL + '/<int:track_id>/show/JSON/')
def singleTrackJSON(artist_id, album_id, track_id):
    track = getTrack(artist_id, album_id, track_id)
    if track:
        return jsonify(Track=[track.serialize])
    else:
        return invalidJSON()

# --- JSON API endpoints end --- #

# --- Simple GET-only pages that only require Read CRUD functionality --- #

# Landing screen - show all artists


@app.route('/')
@app.route('/artists/')
def showArtists():
    artists = getAllArtists()
    return render_template('artists.html', artists=artists)

# Shows the discography for a specific artist, returns invalidRequest()
# if artist_id doesn't exist


@app.route('/artists/<int:artist_id>/')
@app.route('/artists/<int:artist_id>/discography/')
def showDiscography(artist_id):
    artists = getAllArtists()
    artist = getArtist(artist_id)
    albums = getDiscography(artist_id)
    if artist:
        return render_template(
                                'discography.html', artist=artist,
                                albums=albums, artists=artists)
    else:
        return invalidRequest()

# Shows the tracklist for a specific album by a specific artist.
# If the given combination of artist and album ID doesn't exist, returns
# invalidRequest()


@app.route(ALBUM_URL)
@app.route(ALBUM_URL + '/tracklisting')
def showTracklisting(artist_id, album_id):
    tracks = getTracklisting(artist_id, album_id)
    albums = getDiscography(artist_id)
    album = getAlbumInfo(artist_id, album_id)
    if album:
        return render_template(
                                'tracklisting.html', album=album,
                                tracks=tracks, albums=albums)
    else:
        return invalidRequest()

# Shows the track info for a specific track on a specific album, by a specific
# artist. If the given combination of artist, album and track ID doesn't exist,
# returns invalidRequest()


@app.route(ALBUM_URL + '/<int:track_id>/show/')
def showTrack(artist_id, album_id, track_id):
    tracks = getTracklisting(artist_id, album_id)
    track = getTrack(artist_id, album_id, track_id)
    if track:
        return render_template('track_info.html',
                               track=track,
                               tracks=tracks)
    else:
        return invalidRequest()

# --- GET-only pages end -- #

# --- GET/POST pages with Create, Update and Delete CRUD functionality. --- #

# Create a new artist. Checks if the user is logged in, before checking the
# request method. If POST, checks if the artist already exists in the db based
# on artist_id. If not, creates a new entry.


@app.route('/artists/new/', methods=['GET', 'POST'])
def newArtist():
    if 'username' in login_session:
        if request.method == 'POST':
            artist_exists = artistExists(request.form['name'])
            if artist_exists:
                flash("%s already exists" % artist_exists.name)
                return redirect(url_for('newArtist'))
            else:
                return createArtist(request.form, login_session)
        else:
            return render_template('new_artist.html')
    else:
        return notAuth('showArtists', False)

# Updates an existing artist. Checks if the user is logged in, then checks
# if the requested artist exists. If they don't, return invalidRequest(). Then
# checks that the current user is authorized to modify the given artist, and
# returns notAuth if they aren't. The request's new data is checked to see if
# the new artist's name is already in the database, and if so, rejects it and
# redirects back to the original form. If all these test are passed, artist
# data is updated in the db and the user is redirected back to the artists
# page.


@app.route('/artists/<int:artist_id>/edit/', methods=['GET', 'POST'])
def editArtist(artist_id):
    if 'username' in login_session:
        artist = getArtist(artist_id)
        if artist:
            if login_session['user_id'] == artist.user_id:
                if request.method == 'POST':
                    artist_exists = artistExists(
                                                request.form['name'],
                                                artist_id)
                    if artist_exists:
                        flash("%s already exists" % artist_exists.name)
                        return redirect(url_for(
                                                'editArtist',
                                                artist_id=artist_id))
                    else:
                        return updateArtist(artist, request.form)
                else:
                    return render_template('edit_artist.html', artist=artist)
            else:
                return notAuth('showArtists')
        else:
            return invalidRequest()
    else:
        return notAuth('showArtists', False)


# Deletes an  artist. Checks if the user is logged in, then checks
# if the requested artist exists. If they don't, return invalidRequest(). Then
# checks that the current user is authorized to modify the given artist, and
# returns notAuth if they aren't. If these test are passed, artist
# data is deleted, along with all pertinent track and album data, and the
# user is redirected back to the artists page.

@app.route('/artists/<int:artist_id>/delete/', methods=['GET', 'POST'])
def deleteArtist(artist_id):
    if 'username' in login_session:
        artist = getArtist(artist_id)
        if artist:
            if login_session['user_id'] == artist.user_id:
                if request.method == 'POST':
                    return removeArtist(artist)
                else:
                    return render_template('delete_artist.html',
                                           artist=artist)
            else:
                return notAuth('showArtists')
        else:
            return invalidRequest()
    else:
        return notAuth('showArtists', False)

# Nearly identical to the newArtist endpoint; only differences are that here
# we check that the given artist exists before creating an album for them.
# Note that we only check that it doesn't already exist for THAT specific
# artist, to allow for albums with the same name to be written by different
# artist. Beyond that, the user authentication and authorization are exactly
# the same.


@app.route('/artists/<int:artist_id>/discography/new/',
           methods=['GET', 'POST'])
def newAlbum(artist_id):
        if 'username' in login_session:
            artist = getArtist(artist_id)
            if artist:
                if login_session['user_id'] == artist.user_id:
                    if request.method == 'POST':
                        album_exists = albumExists(request.form['name'],
                                                   artist_id)
                        if album_exists:
                            flash("%s by %s already exists" % (
                                request.form['name'], artist.name))
                            return redirect(url_for(
                                                    'newAlbum',
                                                    artist_id=artist_id))
                        else:
                            return createAlbum(request.form, login_session,
                                               artist)
                    else:
                        return render_template('new_album.html',
                                               artist=artist)
                else:
                    return notAuth(
                            'showDiscography', True, artist_id=artist_id)
            else:
                return invalidRequest()
        else:
            return notAuth('showDiscography', False, artist_id=artist_id)

# Again, nearly identical to the editArtist, except that here we update an
# Album. Like the above, checks new data doesn't pre-exist for that album only.


@app.route(ALBUM_URL + '/edit/', methods=['GET', 'POST'])
def editAlbum(artist_id, album_id):
    if 'username' in login_session:
        album = getAlbumInfo(artist_id, album_id)
        if album:
            if login_session['user_id'] == album.user_id:
                if request.method == 'POST':
                    album_exists = albumExists(request.form['name'],
                                               artist_id, album_id)
                    if album_exists:
                        flash("%s by %s already exists" %
                              (album.name, album.artist))
                        return redirect(url_for('editAlbum',
                                        artist_id=artist_id,
                                        album_id=album_id))
                    else:
                        return updateAlbum(album, request.form)
                else:
                    return render_template('edit_album.html', album=album)
            else:
                return notAuth('showDiscography', True, artist_id=artist_id)
        else:
            return invalidRequest()
    else:
        return notAuth('showDiscography', False, artist_id=artist_id)

# Nearly identical to the deleteArtist endpoint; in a similar fashion, upon
# deleting an album, deletes all tracks relating to it.


@app.route(ALBUM_URL + '/delete/', methods=['GET', 'POST'])
def deleteAlbum(artist_id, album_id):
    if 'username' in login_session:
        album = getAlbumInfo(artist_id, album_id)
        if album:
            if login_session['user_id'] == album.user_id:
                if request.method == 'POST':
                    return removeAlbum(album)
                else:
                    return render_template('delete_album.html', album=album)
            else:
                return notAuth('showDiscography', True, artist_id=artist_id)
        else:
            return invalidRequest()
    else:
        return notAuth('showDiscography', False, artist_id=artist_id)

# Very similar to the newAlbum endpoint, only here checks that the given album
# exists and not the artist (since to create the given album the artist would
# have had to exist). Like newAlbum, here we only check that the new track
# doesn't already exist for that album only, to allow for the same track to
# appear on multiple albums for a single artist.


@app.route(ALBUM_URL + '/new/',
           methods=['GET', 'POST'])
def newTrack(artist_id, album_id):
    if 'username' in login_session:
        album = getAlbumInfo(artist_id, album_id)
        if album:
            if login_session['user_id'] == album.user_id:
                if request.method == 'POST':
                    track_exists = trackExists(request.form['name'], album_id)
                    if track_exists:
                        flash("%s already exists on %s by %s" %
                              (track_exists.name, track_exists.album,
                               track_exists.artist))
                        return redirect(url_for('newTrack',
                                                artist_id=artist_id,
                                                album_id=album_id))
                    else:
                        return createTrack(request.form, login_session, album)
                else:
                    return render_template('new_track.html', album=album)
            else:
                return notAuth('showTracklisting', True, artist_id=artist_id,
                               album_id=album_id)
        else:
            return invalidRequest()
    else:
        return notAuth('showTracklisting', False, artist_id=artist_id,
                       album_id=album_id)

# The same as editAlbum, with the same pre-existing data checks from newTrack.


@app.route(ALBUM_URL + '/<int:track_id>/edit/', methods=['GET', 'POST'])
def editTrack(artist_id, album_id, track_id):
    if 'username' in login_session:
        track = getTrack(artist_id, album_id, track_id)
        if track:
            if login_session['user_id'] == track.user_id:
                if request.method == 'POST':
                    track_exists = trackExists(request.form['name'],
                                               album_id, track_id)
                    if track_exists:
                        track = (track_exists.name, track_exists.album,
                                 track_exists.artist)
                        flash("%s already exists on %s by %s" % track)
                        return redirect(url_for('editTrack',
                                                artist_id=artist_id,
                                                album_id=album_id,
                                                track_id=track_id))
                    else:
                        return updateTrack(track, request.form)
                else:
                    return render_template('edit_track.html', track=track)
            else:
                return notAuth('showTracklisting', True, artist_id=artist_id,
                               album_id=album_id)
        else:
            return invalidRequest()
    else:
        return notAuth('showTracklisting', False, artist_id=artist_id,
                       album_id=album_id)

# Deletes a single track using the same checks as normal. Will only delete a
# single track with no related data being affected.


@app.route(ALBUM_URL + '/<int:track_id>/delete/', methods=['GET', 'POST'])
def deleteTrack(artist_id, album_id, track_id):
    if 'username' in login_session:
        track = getTrack(artist_id, album_id, track_id)
        if track:
            if login_session['user_id'] == track.user_id:
                if request.method == 'POST':
                    return removeTrack(track)
                else:
                    return render_template('delete_track.html', track=track)
            else:
                return notAuth('showTracklisting', True, artist_id=artist_id,
                               album_id=album_id)
        else:
            return invalidRequest()
    else:
        return notAuth('showTracklisting', False, artist_id=artist_id,
                       album_id=album_id)

# Helper functions - Authentication & Authorization

# Compiles GET requests and extracts a specific piece of data from the result.
# Args: url (a given url string with interpolation points), num (an integer to
# use as an index value to extract the part of the result we want), *args (all
# variables needed to complete our url string). Combines the url and args to
# form a complete url, before using httplib2's Http() method to make a GET
# request. Then uses num to extract the relevant data, which is then returned.


def http2GETRequest(url, num, *args):
    url = url % (args)
    h = httplib2.Http()
    result = h.request(url, 'GET')[num]
    return result

# Compiles responses for client-side AJAX calls after handling.
# Args: login_session (contains newly-acquired user data to be inserted into
# our string). Inserts user-data from login_session into our pre-existing
# html string template before returning it.


def renderOutput(login_session):
    output = ''
    output += '<h2 class="flex-center-align">Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " class="login-img flex-center-align"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# Creates a new user in the db
# Args: login_session (contains newly-acquired user data to insert into the db)
# Creates a new User instance, which is then added to the session and commited.
# Then fetches the new user from the database and returns their id.


def createUser(login_session):
    newUser = User(
                name=login_session['username'],
                email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).first()
    return user.id

# Fetches a user from the db using a given id
# Args: user_id
# Executes an SQL query using sqlalchemy to fetch a user object based on
# user_id, and returns it.


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Fetches a user's ID based on their email address
# Args: email
# attempts to fetch a user from the db, and if successful, returns their id.
# If not, returns None.


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Generates a flash message depending on authorization before redirecting
# Args: endpoint (the target endpoint to redirect to after generating flash
# message), unauthorized (Boolean to determine flash message), **kwargs (may
# be needed to render endpoint)
# Checks unauthorized's value and generates a flash message. False doesn't
# mean authorized necessarily, as this also applies when the user is not
# logged in. It just means 'not unauthorized' (because it doesn't know that
# are). Redirects to the given endpoint using kwargs if need be.


def notAuth(endpoint, unauthorized=True, **kwargs):
    if unauthorized:
        flash('You are not authorized to do that.')
    else:
        flash('You must be logged in to do that.')
    return redirect(url_for(endpoint, **kwargs))

# Fallback response if a bad url is requested (e.g. a request to view an
# album by an artist that doesn't relate to them, or an artist that doesn't
# exist)
# Generates a flash message and redirects to the home page.


def invalidRequest():
    flash("Invalid Request")
    return redirect(url_for('showArtists'))

# As above but for JSON


def invalidJSON():
    response = make_response(json.dumps('Invalid Request.'), 400)
    response.headers['Content-Type'] = 'application/json'
    return response


# Helper functions - Read items from the db
# Fetches all Artists in the db


def getAllArtists():
    return session.query(Artist).order_by(Artist.name).all()

# Fetches a specific Artist from the db. Uses first() instead of one(),
# so that if they don't exist it will return empty and not throw an error.
# Empty objects are mostly handled in templates by jinja2.


def getArtist(artist_id):
    return session.query(Artist).filter_by(id=artist_id).first()

# Fetches the full discography for a specific based on artist_id


def getDiscography(artist_id):
    return session.query(Album).filter_by(
                                artist_id=artist_id).order_by(
                                Album.year.desc()).all()

# Fetches an album's tracklisting based on artist and album id.
# Checks for both to prevent a bad request (invalidRequest(0) will be called
# if so)


def getTracklisting(artist_id, album_id):
    return session.query(Track).filter_by(
                                artist_id=artist_id,
                                album_id=album_id).order_by(
                                Track.num).all()

# Fetches a single album's information from the db (not its tracks).
# Again, checks artist and album id to avoid a bad request.


def getAlbumInfo(artist_id, album_id):
    return session.query(Album).filter_by(
                                artist_id=artist_id,
                                id=album_id).first()

# Fetches a single track's information from the db.
# This time artist, album and track id are all checked for validity.


def getTrack(artist_id, album_id, track_id):
    return session.query(Track).filter_by(
                                artist_id=artist_id,
                                album_id=album_id,
                                id=track_id).first()


# Helper functions - Create, Update & Delete Items

# Checks if an artist with the given name already exists in the db
# Args: name (a string a newly submitted data to be checked),
# artist_id (optional: needed if updating an existing value rather than
# creating a new one, so that the data we're updating can be filtered out)
# Uses sqlalchemy to submit an SQL query checking if the given name exists,
# based on name and artist_id (if given). Will return an object regardless,
# but if the value does not exist in the db this object will be empty.


def artistExists(name, artist_id=""):
    if artist_id:
        exists = session.query(Artist).filter(
                                        Artist.id != artist_id,
                                        Artist.name == name).first()
    else:
        exists = session.query(Artist).filter_by(
                                        name=request.form['name']).first()
    return exists

# Like the above, only this time checks for an album by a specific artist.
# Args: name (string to be checked), artist_id (required to check only albums
# by the given artist, since duplicate album names by different artists are
# allowed), album_id (optionalL only required to check if we're updating not
# creating)
# Functions in the same way as the above, only now also filters on artist name
# as well to avoid albums by other artists potentially being returned.


def albumExists(name, artist_id, album_id=""):
    if album_id:
        exists = session.query(Album).filter(
                                    Album.id != album_id,
                                    Album.artist_id == artist_id,
                                    Album.name == name).first()
    else:
        exists = session.query(Album).filter(
                                    Album.artist_id == artist_id,
                                    Album.name == name).first()
    return exists

# The same as the previous two, but this time uses a specific album to filter
# Args: name (string to be checked), album_id (compulsory to check
# our track doesn't already exist on this specific album)
# Functions in the same way as the above, only filters using an album_id
# instead of an artist one. Artist will already be unique to this album so we
# don't need to filter on this as well


def trackExists(name, album_id, track_id=""):
    if track_id:
        exists = session.query(Track).filter(
                                Track.id != track_id,
                                Track.album_id == album_id,
                                Track.name == name).first()
    else:
        exists = session.query(Track).filter(
                                Track.album_id == album_id,
                                Track.name == name,).first()
    return exists

# Creates a new artist in the db
# Args: form (object submitted in request object), login_session (needed to
# record which user added the artist for authorization later)
# Creates an Artist instancer in session using the given objects, generates a
# flash confirmation message and returns a redirect for the home page.


def createArtist(form, login_session):
    newArtist = Artist(name=form['name'],
                       image=form['image'],
                       user_id=login_session['user_id'])
    session.add(newArtist)
    session.commit()
    flash("%s Added" % newArtist.name)
    return redirect(url_for('showArtists'))

# Creates a new album in the db
# Args: form (object submitted in request object), login_session (needed to
# record which user added the album for authorization later), artist (to
# record which artist the album relates to)
# Creates an Album instance in session using the given objects, generates a
# flash confirmation message and returns a redirect for the home page.


def createAlbum(form, login_session, artist):
    newAlbum = Album(
                    name=form['name'],
                    artist=artist.name,
                    artist_id=artist.id,
                    year=form['year'],
                    genre=form['genre'],
                    artwork=form['artwork'],
                    user_id=login_session['user_id'])
    session.add(newAlbum)
    session.commit()
    flash("%s has been added" % newAlbum.name)
    return redirect(url_for('showDiscography',
                            artist_id=newAlbum.artist_id))

# Creates a new track in the db
# Args: form (object submitted in request object), login_session (needed to
# record which user added the track for authorization later), album (to
# record which album and artist the track relates to)
# Creates an Album instance in session using the given objects, generates a
# flash confirmation message and returns a redirect for the home page.


def createTrack(form, login_session, album):
    newTrack = Track(name=form['name'],
                     num=form['number'],
                     artist=album.artist,
                     album=album.name,
                     artist_id=album.artist_id,
                     album_id=album.id,
                     user_id=login_session['user_id'])
    session.add(newTrack)
    session.commit()
    flash("%s added successfully" % newTrack.name)
    return redirect(url_for('showTracklisting',
                    artist_id=newTrack.artist_id,
                    album_id=newTrack.album_id))

# Updates an existing artist in the db
# Args: artist (artist object from the db to be updated), form (object
# submitted in request object)
# Updates the given artist object with submitted data in the form object.
# Note that only client-side data can be updated; db-dependent values such as
# id and user_id are permanent. Users can work around this by deleting the
# artist and creating a new entry.


def updateArtist(artist, form):
    artist.name = form['name']
    artist.image = form['image']
    session.add(artist)
    session.commit()
    flash("%s updated successfully" % artist.name)
    return redirect(url_for('showArtists'))

# Updates an existing album in the db
# Args: album (artist object from the db to be updated), form (object
# submitted in request object)
# Updates the given album object with submitted data in the form object.
# Note that only client-side data can be updated; db-dependent values such as
# id and user_id are permanent. This includes what artist the album relates to,
# to avoid further complications. Users can work around this by deleting the
# artist and creating a new entry.


def updateAlbum(album, form):
    album.name = form['name']
    album.year = form['year']
    album.genre = form['genre']
    album.artwork = form['artwork']
    session.add(album)
    session.commit()
    flash("%s updated successfully" % album.name)
    return redirect(url_for('showDiscography',
                    artist_id=album.artist_id))

# Updates an existing album in the db
# Args: album (artist object from the db to be updated), form (object
# submitted in request object)
# Updates the given album object with submitted data in the form object.
# Note that only client-side data can be updated; db-dependent values such as
# user_id are permanent. This includes what artist and album relates it to,
# to avoid further complications. Users can work around this by deleting the
# artist and creating a new entry.


def updateTrack(track, form):
    track.name = form['name']
    track.num = form['number']
    session.add(track)
    session.commit()
    flash("%s Updated Successfully" % track.name)
    return redirect(url_for('showTracklisting',
                    artist_id=track.artist_id,
                    album_id=track.album_id))

# Removes an Artist from the db, including all related data
# Args: artist (object to be removed from the db, also used to reference
# secondary data to be deleted)
# First removes all tracks relating to the artist, followed by all albums,
# before deleting the artist themselves. Generates a flash message to confirm
# before redirecting.


def removeArtist(artist):
    session.query(Track).filter_by(artist_id=artist.id).delete()
    session.query(Album).filter_by(artist_id=artist.id).delete()
    session.delete(artist)
    session.commit()
    flash("%s, their albums and tracks have all been deleted successfully"
          % artist.name)
    return redirect(url_for('showArtists'))

# Removes an Album from the db, including all related data
# Args: album (object to be removed from the db, also used to reference
# secondary data to be deleted)
# First removes all tracks relating to the album, before deleting the album
# itself. Generates a flash message to confirm before redirecting.


def removeAlbum(album):
    session.query(Track).filter_by(album_id=album.id).delete()
    session.delete(album)
    session.commit()
    flash("%s and its tracks have been deleted successfully"
          % album.name)
    return redirect(url_for('showDiscography',
                            artist_id=album.artist_id))

# Removes a Track from the db
# Args: track (object to be removed from the db)
# Removes the track from the db, before generating flash confirmation
# and redirecting.


def removeTrack(track):
    session.delete(track)
    session.commit()
    flash("%s deleted successfully" % track.name)
    return redirect(url_for('showTracklisting',
                            artist_id=track.artist_id,
                            album_id=track.album_id))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=80)
