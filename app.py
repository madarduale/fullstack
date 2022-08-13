#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from distutils.log import error
from email import message
import imp
from itertools import count
import json
from typing import final
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,abort
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging  
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import desc
from models import  db,Artist, Venue, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
# db=SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect()
csrf.init_app(app)




# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
      date = dateutil.parser.parse(value)
  else:
      date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data=Venue.query.order_by(Venue.id.desc()).limit(10).all()
  group_by_city_state = {}
  for venue in data:
    city_state = venue.city + ', ' + venue.state
    if city_state not in group_by_city_state:
      group_by_city_state[city_state] = []
    group_by_city_state[city_state].append(venue)


 


  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  return render_template('pages/venues.html', areas=group_by_city_state);

@app.route('/venues/search', methods=['POST'])
@csrf.exempt
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search = request.form.get('search_term')
  data = Venue.query.filter(Venue.name.ilike(f'%{search}%')).all() or Venue.query.filter(Venue.city.ilike(f'%{search}%')).all() or Venue.query.filter(Venue.state.ilike(f'%{search}%')).all()
  count = len(data)

  return render_template('pages/search_venues.html', results=data, search_term=search, count=count)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    data=Venue.query.get(venue_id)
    past_shows_query=db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
    upcoming_shows_query=db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>=datetime.now()).all()
    past_shows=[]
    upcoming_shows=[]
    for show in past_shows_query:
      past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })
    for show in upcoming_shows_query:
      upcoming_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })
    upcoming_shows_count=len(upcoming_shows)
    past_shows_count=len(past_shows)
    data1={
      "id": data.id,
      "name": data.name,
      "genres": data.genres,
      "city": data.city,
      "state": data.state,
      "address": data.address,
      "phone": data.phone,
      "website": data.website,
      "facebook_link": data.facebook_link,
      "seeking_talent": data.seeking_talent,
      "seeking_description": data.seeking_description,
      "image_link": data.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": past_shows_count,
      "upcoming_shows_count": upcoming_shows_count,
     }
  


    return render_template('pages/show_venue.html', venue=data1)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()

  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
@csrf.exempt
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  form = VenueForm()
  if form.validate_on_submit():
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      website=form.website.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data
    )
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # return redirect(url_for('index'))
  else:
    for field , message in form.errors.items():
      flash(field+ '->' + str(message),'Danger')
  return render_template('pages/home.html')







  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/delet/<venue_id>/', methods=['POST'])
@csrf.exempt
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error=False
  venue=Venue.query.get(venue_id)
  show_delete=Show.query.filter(Show.venue_id==venue_id).all()
  for show in show_delete:
    db.session.delete(show)
  db.session.delete(venue)
  try:
    db.session.commit() 
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
    return redirect(url_for('index'))
  else:
    flash('Venue ' + venue.name + ' was successfully deleted!')
    return redirect(url_for('index'))

  





#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.order_by(desc(Artist.id)).all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
@csrf.exempt
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    search = request.form.get('search_term')
    data = Artist.query.filter(Artist.name.ilike(f'%{search}%')).all() or Artist.query.filter(Artist.city.ilike(f'%{search}%')).all() or Artist.query.filter(Artist.state.ilike(f'%{search}%')).all()
    count = len(data)

    return render_template('pages/search_artists.html', results=data, search_term=search,count=count)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  past_shows_query=db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
  upcoming_shows_query=db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time>=datetime.now()).all()
  data=Artist.query.get(artist_id)
  past_shows=[]
  upcoming_shows=[]
  for show in past_shows_query:
      past_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time
      })
  for show in upcoming_shows_query:
      upcoming_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time
      })
  upcoming_shows_count=len(upcoming_shows)
  past_shows_count=len(past_shows)
  data1={
      "id": data.id,
      "name": data.name,
      "genres": data.genres,
      "city": data.city,
      "state": data.state,
      "phone": data.phone,
      "website": data.website,
      "facebook_link": data.facebook_link,
      "seeking_talent": data.seeking_venue,
      "seeking_description": data.seeking_description,
      "image_link": data.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": past_shows_count,
      "upcoming_shows_count": upcoming_shows_count,
     
  }
  


  return render_template('pages/show_artist.html', artist=data1)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
 
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
@csrf.exempt
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  form = ArtistForm()
  error = False
  if request.method=='POST':
    try:
      artist.name = form.name.data
      artist.genres = form.genres.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.facebook_link = form.facebook_link.data
      artist.website = form.website.data
      artist.image_link = form.image_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      db.session.commit()
    except Exception:
      error = True
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      abort(400)
    else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
@csrf.exempt
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  venue = Venue.query.get(venue_id)
  form = VenueForm()

  if request.method == 'POST':
    try:
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.phone = form.phone.data
      venue.address = form.address.data
      venue.genres = form.genres.data
      venue.facebook_link = form.facebook_link.data
      venue.website = form.website.data
      venue.image_link = form.image_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data
      db.session.commit()
    except Exception:
      db.session.rollback()
    finally:
      db.session.close()
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
      
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
@csrf.exempt
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  form = ArtistForm()

  if form.validate_on_submit():
    try:
      artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        website=form.website.data,
        image_link=form.image_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data
      )
      db.session.add(artist)
      db.session.commit()
    except Exception:
      db.session.rollback()
    finally:
      db.session.close()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      return redirect(url_for('index'))
  else:
   for field, message in form.errors.items():
    
        flash(field+': '+str(message), 'danger')
  return render_template('forms/new_artist.html', form=form)



  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data= Show.query.order_by(desc(Show.id)).all()
 
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
@csrf.exempt
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  form = ShowForm()
  if form.validate_on_submit():
    try:
      show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data
      )
      db.session.add(show)
      db.session.commit()
    except Exception:
      db.session.rollback()
    finally:
      db.session.close()
      flash('Show was successfully listed!')
      return redirect(url_for('index'))
  else:
    for field, message in form.errors.items():
      flash(field+': '+str(message), 'danger')
  return render_template('forms/new_show.html', form=form)


 
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
