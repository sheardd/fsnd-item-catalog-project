README - Item Catalog Project for Udacity
==============================================================================

Directory Contents and Description

------------------------------------------------------------------------------

main.py

Summary:
Our primary handlers and functions file, called to handle all requests and
serve all responses. Based on Udacity's oauth vm's project.py, then expanded on
and modified.


Dependencies:

all template files (artists.html, base.html, delete_album.html,
delete_artist.html, delete_track.html, discography.html, edit_album.html, 
edit_artist.html, edit_track.html, header.html, login.html, new_album.html,
new_artist.html, new_track.html, track_info.html, tracklisting.html)

database_setup.py

client_secrets.json
fb_client_secrets.json
(contain app-specific credentials for API calls)


Imported Modules:

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
(various flask functions to access template building, request data, redirecting
to alternative endpoints and converting objects to JSON, as well as the Flask
object to interface with the db)

from sqlalchemy import create_engine, asc, and_
(required to interface easily with the db, with some additions to improve filter
and order functionality)

from sqlalchemy.orm import sessionmaker
(as above)

from database_setup import Base, User, Artist, Album, Track
(allows us to create new instances to insert into the db, as well as update
or delete data)

from flask import session as login_session
(as above)

import random
(used to generate random values for secure STATE tokens)

import string
(used to split strings to extract values, such as in urls)

from oauth2client.client import flow_from_clientsecrets
(used to get client_secret data from our client_secret JSON objects)

from oauth2client.client import FlowExchangeError
(used for error handling if our token upgrade with google+ fails)

import httplib2
(used to make API calls)

import json
(used in our API endpoints to return JSON)

from flask import make_response
(used to respond to AJAX requets when user logs in)

import requests

------------------------------------------------------------------------------

database_setup.py

Summary:
Contains Classes for all tables to be used in our db, which can be used to
create, read, update or delete data. When run in the terminal, will also create
our mitunes.db database file.

Dependencies:
None

Imported Modules:

from sqlalchemy import Column, ForeignKey, Integer, String
(required to create our Classes for our tables, as well as assign them columns
and string or integer types and assign ForeignKey to relationships)

from sqlalchemy.ext.declarative import declarative_base
(required as a parent Class for all our own Classes)

from sqlalchemy.orm import relationship
(required to create relationships between columns in tables)

from sqlalchemy import create_engine
(required to create our db and interface with it using our Classes)


------------------------------------------------------------------------------

populate.py

Summary:
Contains instances of data compatible with mitunes.db that will be added to the 
database when run in the terminal.

Dependencies:
database_setup.py

Imported Modules:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
(required to interface with our database using our Classes)

from database_setup import Base, User, Artist, Album, Track
(allows us to create new instances to insert into the db)


------------------------------------------------------------------------------
templates/

Contents: Eight html template files, used to render dynamic pages (full list
below)

	1) index.html - Our base template, including user-sensitive footer.
	2) blog-feed.html - The front page of the site, displaying all posts and
						comments.
	3) blog-newpost.html - Our form to submit new blog posts.
	4) blog-permalink.html - Displays an individual blog post on request or
						successful submission of a new post.
	5) blog-editpost.html - Similar to blog-newpost.html, but with different
						actions to handle data differently
	6) login.html - Simple form to submit login credentials.
	7) user-signup.html - Extended version of login.html with different
						handlers to evaluate and create new users.
	8) welcome.html - A simple welcome screen rendered upon successful
						submission of login or signup details.

Dependencies: All templates are extensions of index.html. Templates also
require jinja2 for variable substitution to generate pages with user data.
index.html also calls some fonts from google fonts, but fallback fonts have
been provided if these cannot be rendered for some reason. Likewise, index.html
also calls main.css for styling, but the page will run without it.

------------------------------------------------------------------------------

main.css

Summary: A very basic site-wide stylesheet.

Dependencies: Called by index.html, referenced in app.yaml, references some
google fonts linked at the start of index.html (to apply to all other
templates), but fallback values have been provided so the stylesheet can
function without if necessary.

==============================================================================

Quick-Start Guide

------------------------------------------------------------------------------

In order to host this application, it must be run either from a server or a
virtual machine. To do this, some basic working knowledge of the command line
is required.

1) In order to host the application locally, first you need to install git,
which can be downloaded here:
	https://git-scm.com/downloads

2) You also need to download virtualbox from here:
	https://www.virtualbox.org/wiki/Downloads

2) Next, install vagrant from here:
	https://www.vagrantup.com/downloads.html

3) You'll need a virtual machine to run using the installed software. This
project was created using the udacity oauth VM available here (possibly only
available to udacity students)
	- Decide where on your computer you want to install the virtual machine,
	  then enter the command terminal, cd to that directory and type:
	  	"git clone https://github.com/udacity/OAuth2.0 oauth"
	- Now cd into the oauth directory you just created and type:
		"vagrant up"
	- Once the machine has launched, type "vagrant ssh" to sign into it.
	- To access the shared folder for this machine (shared between your
	  virtual machine and your actual one), type "cd /vagrant/"
	- You can now copy and paste this application into the oauth directory,
	  and they should be visible in this command line when you type "ls".
	- You're now ready to install the application on your newly-minted vm!
	

Preparing the application to host:

1) Open the command line and type
	"cd <ENTER THE FILE PATH OF THIS FOLDER HERE>"

2) Now that you're in the right folder in the command line, type the following
two commands:
	"python database_setup.py"
	"python populate.py"

3) Your application should now have a database with some sample data in. If
you're running this application on a VM, you can start serving the application
locally by typing:
	"python main.py"

4) The application will now be viewable in the browser at http://localhost:5000/


