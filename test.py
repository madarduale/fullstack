from sqlalchemy import func
from itertools import count
from app import  db, Artist, Venue, Show
from datetime import datetime, timedelta, date, time, timezone

# def create_artist(id,name, city, state, phone, genres, image_link,seeking_venue):
#     artist = Artist(id=id,name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link, seeking_venue=seeking_venue)
#     db.session.add(artist)
#     db.session.commit()
#     return artist
# create_artist("Guns N' Roses", "San Francisco", "CA", "326-123-4567", ["Rock n Roll"], "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80", "https://www.facebook.com/GunsNRoses", "http://www.gunsnroses.com", True, "We are looking for a guitarist.")
# create_artist(4,"Guns N Petals","San Francisco","CA","326-123-5000",["Rock n Roll"], "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80","https://www.facebook.com/GunsNPetals","https://www.gunsnpetalsband.com",True,"Looking for shows to perform at in the San Francisco Bay Area!",)
# create_artist(5,"Matt Quevedo","New York","NY","300-400-5000", ["Jazz"],"https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80","https://www.facebook.com/mattquevedo923251523",False)
# create_artist(6,"The Wild Sax Band","San Francisco","CA","432-325-5432", ["Jazz", "Classical"],"https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",False)

# def creat_venue(name, city, state, address, phone, genres, image_link, facebook_link, website, seeking_talent,):
#     venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link, website=website, seeking_talent=seeking_talent)
#     db.session.add(venue)
#     db.session.commit()
#     return venue
# creat_venue("The Musical Hop", "San Francisco", "CA", "1015 Folsom Street", "123-123-1234", ["Jazz", "Reggae", "Swing", "Classical", "Folk"], "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60", "https://www.facebook.com/TheMusicalHop", "http://www.themusicalhop.com", True, "We are on the lookout for a local artist to play every two weeks. Please call us.")
# creat_venue("The Dueling Pianos Bar","New York","NY","335 Delancey Street","914-003-1132",["Classical", "R&B", "Hip-Hop"],"https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80","https://www.facebook.com/theduelingpianos","https://www.theduelingpianos.com",False)

# creat_venue( "Park Square Live Music & Coffee","San Francisco", "CA","34 Whiskey Moore Ave", "415-000-1234",["Rock n Roll", "Jazz", "Classical", "Folk"],"https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80", "https://www.facebook.com/ParkSquareLiveMusicAndCoffee","https://www.parksquarelivemusicandcoffee.com",False)

# def create_show(id,artist_id, venue_id, start_time):
#     show = Show(id=id,artist_id=artist_id, venue_id=venue_id, start_time=start_time)
#     db.session.add(show)
#     db.session.commit()
#     return show
# create_show(4, 1,"2019-05-21T21:30:00.000Z" )   
# create_show(2,5, 3,"2019-06-15T23:00:00.000Z" )
# create_show(6, 3,"2035-04-01T20:00:00.000Z" )
# create_show(6, 3,"2035-04-08T20:00:00.000Z" )
# create_show(6, 3, "2035-04-15T20:00:00.000Z")


# def show_venue():
    # venues = Venue.query.all()
    # print(venue.venues)
    # today = datetime.now()
    # print("today",today)
    # dt_string = today.strftime("%d/%m/%Y %H:%M:%S")
    # print("date and time =", dt_string)	
    # for show in venue.venues:
    #     print(show.artist.name)
    #     print(show.start_time)
    #     print(show.venue.name)
    # for venye in venue.shows:
    #     print(venye.artist.name)
    #     print(venye.start_time)
    #     print(venye.venue.name)
    
    # shows = Show.query.all()
    # for show in shows:
    #     if show.start_time >= today:
    #         print("upcoming show:")
    #         print(show.artist.name)
    #         print(show.start_time)
    #         print(show.venue.name)
    #         print("\n")
    #     elif show.start_time < today:
    #         print("past show:")
    #         print(show.artist.name)
    #         print(show.start_time)
    #         print(show.venue.name)
    #         print("\n")

    # for venue in venues:
    #         print(venue)
    #         print(venue.name)
            # print(venue.city)
            # print(venue.state)
            # print(venue.phone)
            # # print(venue.genres)
            # for genre in venue.genres:
            #     print(genre)
            # print(venue.address)
            # print(venue.seeking_talent)
            # print(venue.image_link)
            # print(venue.website)
            # print(venue.seeking_description)
            # print(venue.facebook_link)
            # print(venue.shows)
   


            # countpast=0
            # countupcoming=0
            # for show in venue.shows:
            #     if show.start_time >= today:
            #         countupcoming+=1
            #         print("upcoming show:")
            #         print(show.artist.name)
            #         print(show.start_time)
            #         print(show.venue.name)
            #         print("\n")
            #     elif show.start_time < today:
            #         countpast+=1
            #         print("past show:")
            #         print(show.artist.name)
            #         print(show.start_time)
            #         print(show.venue.name)
            #         print("\n")
            #     print("\n")
            # print(countpast)
            # print(countupcoming)

# upcoming=''
# past=''
#     shows=Show.query.filter_by(venue_id=3).all()
#     upcomings=[]
#     pasts=[]
#     for show in shows:
#     #     print(show.start_time)
#         if show.start_time>=datetime.now():
#             upcomings.append(show)
#             for upcoming in upcomings:
                
#                 print("upcoming",upcoming.artist.name)
#         else:
#             pasts.append(show)
#             for past in pasts:
#                 print("past",past.artist.name)
            
#     search = 'music'
#     data = Venue.query.filter(Venue.name.ilike(f'%{search}%')).all()
#     for venue in data:
#         print(venue.name)
#     # print(data)
#     count = len(data)
#     print(count)
# show_venue()

# limit =Venue.query.order_by(Venue.id.desc()).limit(10).all()
# group_by_city = {}
# group_by_state = {}
# for venue in limit:
#     city = venue.city
#     state = venue.state
    
#     if city not in group_by_city and state not in group_by_state:
#         group_by_city[city] = []
#         group_by_state[state] = []
#         group_by_city[city].append(venue)
#         group_by_state[state].append(venue)
# print(group_by_city)
# print(group_by_state)
# for city_state, venues in group_by_city.items():
#     print(city_state)
#     for venue in venues:
#         print(venue.name)
#         print(venue.id)
#         # print(venue.city)
#         print("\n")

# group_by_state = {}
# for venue in limit:
#     if venue.state not in group_by_state:
#         group_by_state[venue.state] = []
#     group_by_state[venue.state].append(venue)

# print(group_by_state)
# for state, venues in group_by_state.items():
#     print(state)
#     for venue in venues:
#         print(venue.name)
#         print(venue.id)
#         # print(venue.city)
#         print("\n")



#Venues  display in groups by city and state (if applicable), and display the number of shows per venue.





def search_venue_by_city_state():
    search = 'SAN'
    data = Venue.query.filter(Venue.name.ilike(f'%{search}%')).all() or Venue.query.filter(Venue.city.ilike(f'%{search}%')).all() or Venue.query.filter(Venue.state.ilike(f'%{search}%')).all()
    print(data)
    for venue in data:
        print(venue.name)
    # print(data)
    count = len(data)
    print(count)
search_venue_by_city_state()