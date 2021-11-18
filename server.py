
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.74.246.148/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@34.74.246.148/proj1part2"
#
DATABASEURI = "postgresql://arb2280:8173@34.74.246.148/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
'''
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)
'''

@app.route('/')
def welcome():
    return render_template("welcome.html")
#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#

@app.route('/signin', methods = ["GET", "POST"]) #<username>
def signin():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        print(username)
        
        login = []
        try: 
            cursor = g.conn.execute('SELECT username FROM Users_Contact_Info_Has_Contact_Info WHERE username = (%s) AND password = (%s)', username, password)
            for result in cursor:
                login.append(result['username'])  # can also be accessed using result[0]
            cursor.close()
            
        except Exception:
            error = 'Invalid search query'
        if len(login) == 1:
            return redirect(url_for('home',user = username))
        
        error = 'Invalid username or password'
        
    return render_template("signin.html", error = error)
            
# url should look like home?user=<abc>
@app.route('/home')
def home():
    username = request.args.get('user')
    print(username)
    error = None
    name_list = []
    profile_picture_list = []
    
    try:
        cursor = g.conn.execute('SELECT name, profile_picture FROM Users_Contact_Info_Has_Contact_Info WHERE username = (%s)', username)
        for result in cursor:
            name_list.append(result['name'])
            profile_picture_list.append(result['profile_picture'])
        cursor.close()
        name = name_list[0]
        profile_picture = profile_picture_list[0]
    except Exception:
        error = 'Invalid search query'
        
    has_backyard_list = []
    has_children_list = []
    has_other_pets_list = []
    allows_dropoffs_list = []
    
    print('what')
    try:
        print('helllo')
        cursor = g.conn.execute('SELECT has_backyard, has_children, has_other_pets, allows_dropoffs FROM Will_Host WHERE username = (%s)', username)
        print('wow')
        for result in cursor:
            has_backyard_list.append(result['has_backyard'])
            print(has_backyard_list)
            has_children_list.append(result['has_children'])
            print(has_children_list)
            has_other_pets_list.append(result['has_other_pets'])
            allows_dropoffs_list.append(result['allows_dropoffs'])
            
        print(has_backyard_list)
        
        cursor.close()
        print(len(has_backyard_list))
        if len(has_backyard_list) != 0:
            backyard = has_backyard_list[0]
            print(backyard)
            children = has_children_list[0]
            has_other_pets = has_other_pets_list[0]
            allows_dropoffs = allows_dropoffs_list[0]
        
        else:
            backyard = 'Is not willing to host'
            children = ""
            has_other_pets = ""
            allows_dropoffs = ""
            
    except Exception:
        error = 'Will host'
        
        
    mile_list = []
    carpool_list = []
    try:
        cursor = g.conn.execute('SELECT mile_radius, will_carpool FROM Will_Travel WHERE username = (%s)', username)
        for result in cursor:
            mile_list.append(result['mile_radius'])
            carpool_list.append(result['will_carpool'])
        cursor.close()
        if len(mile_list) != 0:
            mile = mile_list[0]
            carpool = carpool_list[0]
        
        else:
            mile = 'Is not willing to travel'
            carpool = ""
            
    except Exception:
        error = 'Will host'
    
    street_list = []
    city_list = []
    state_list = []
    zip_list = []
    try:
        cursor = g.conn.execute('SELECT A.street_address, A.city, A.state, A.zip FROM Address A, Resides_In R WHERE R.username = (%s) AND A.zip = R.zip AND A.street_address = R.street_address', username)
        for result in cursor:
            street_list.append(result['street_address'])
            city_list.append(result['city'])
            state_list.append(result['state'])
            zip_list.append(result['zip'])
        cursor.close()
        street = street_list[0]
        city = state_list[0]
        state = state_list[0]
        zip = zip_list[0]
            
    except Exception:
        error = 'Address'
    
    free_day_list = []
    free_time_start_list = []
    free_time_end_list = []
    try:
        cursor = g.conn.execute('SELECT free_day, free_time_start, free_time_end FROM Is_Free WHERE username = (%s)', username)
        for result in cursor:
            free_day_list.append(result['free_day'])
            free_time_start_list.append(result['free_time_start'])
            free_time_end_list.append(result['free_time_end'])
        cursor.close()
        
        context_day = dict(free_day = free_day_list)
        context_start = dict(free_time_start = free_time_start_list)
        context_end = dict(free_time_end = free_time_end_list)
        
    except Exception:
        error = 'Free time Query failed'
        
                  
    return render_template("home.html", user = username, name = name, profile_picture = profile_picture, has_backyard = backyard, has_children = children, has_other_pets = has_other_pets, allows_dropoffs = allows_dropoffs, mile_radius = mile, will_carpool = carpool, street_address = street, city = city, state = state, zip = zip, **context_day, **context_start, **context_end)

@app.route('/user2Home')
def user2Home():
    username = request.args.get('user')
    user2 = request.args.get('user2')
    dog2 = request.args.get('dog2')
    print(username)
    print(user2)
    print(dog2)
    error = None
    name_list = []
    profile_picture_list = []
    
    try:
        cursor = g.conn.execute('SELECT name, profile_picture FROM Users_Contact_Info_Has_Contact_Info WHERE username = (%s)', user2)
        for result in cursor:
            name_list.append(result['name'])
            profile_picture_list.append(result['profile_picture'])
        cursor.close()
        name = name_list[0]
        profile_picture = profile_picture_list[0]
    except Exception:
        error = 'Invalid search query'
        
    has_backyard_list = []
    has_children_list = []
    has_other_pets_list = []
    allows_dropoffs_list = []
    
    try:
        cursor = g.conn.execute('SELECT has_backyard, has_children, has_other_pets, allows_dropoffs FROM Will_Host WHERE username = (%s)', user2)
        for result in cursor:
            has_backyard_list.append(result['has_backyard'])
            print(has_backyard_list)
            has_children_list.append(result['has_children'])
            print(has_children_list)
            has_other_pets_list.append(result['has_other_pets'])
            allows_dropoffs_list.append(result['allows_dropoffs'])
            
        print(has_backyard_list)
        
        cursor.close()
        print(len(has_backyard_list))
        if len(has_backyard_list) != 0:
            backyard = has_backyard_list[0]
            print(backyard)
            children = has_children_list[0]
            has_other_pets = has_other_pets_list[0]
            allows_dropoffs = allows_dropoffs_list[0]
        
        else:
            backyard = 'Is not willing to host'
            children = ""
            has_other_pets = ""
            allows_dropoffs = ""
            
    except Exception:
        error = 'Will host'
        
        
    mile_list = []
    carpool_list = []
    try:
        cursor = g.conn.execute('SELECT mile_radius, will_carpool FROM Will_Travel WHERE username = (%s)', user2)
        for result in cursor:
            mile_list.append(result['mile_radius'])
            carpool_list.append(result['will_carpool'])
        cursor.close()
        if len(mile_list) != 0:
            mile = mile_list[0]
            carpool = carpool_list[0]
        
        else:
            mile = 'Is not willing to travel'
            carpool = ""
            
    except Exception:
        error = 'Will host'
    
    street_list = []
    city_list = []
    state_list = []
    zip_list = []
    try:
        cursor = g.conn.execute('SELECT A.street_address, A.city, A.state, A.zip FROM Address A, Resides_In R WHERE R.username = (%s) AND A.zip = R.zip AND A.street_address = R.street_address', user2)
        for result in cursor:
            street_list.append(result['street_address'])
            city_list.append(result['city'])
            state_list.append(result['state'])
            zip_list.append(result['zip'])
        cursor.close()
        street = street_list[0]
        city = state_list[0]
        state = state_list[0]
        zip = zip_list[0]
            
    except Exception:
        error = 'Address'
    
    free_day_list = []
    free_time_start_list = []
    free_time_end_list = []
    try:
        cursor = g.conn.execute('SELECT free_day, free_time_start, free_time_end FROM Is_Free WHERE username = (%s)', user2)
        for result in cursor:
            free_day_list.append(result['free_day'])
            free_time_start_list.append(result['free_time_start'])
            free_time_end_list.append(result['free_time_end'])
        cursor.close()
        
        context_day = dict(free_day = free_day_list)
        context_start = dict(free_time_start = free_time_start_list)
        context_end = dict(free_time_end = free_time_end_list)
        
    except Exception:
        error = 'Free time Query failed'
        
                  
    return render_template("user2Home.html", user = username, user2 = user2, name = name, profile_picture = profile_picture, has_backyard = backyard, has_children = children, has_other_pets = has_other_pets, allows_dropoffs = allows_dropoffs, mile_radius = mile, will_carpool = carpool, street_address = street, city = city, state = state, zip = zip, **context_day, **context_start, **context_end)


@app.route('/addAcc', methods = ["GET", "POST"])
def addAcc():
	username = request.args.get('user')
	name = request.args.get('name')
	error = None
	
	if request.method == "POST":
		username = request.form['user']
		name = request.form['name']
		accommodation_id = request.form['accommodation']
        #accommodation_id = request.form['accommodation']
		try:
			cursor = g.conn.execute('INSERT INTO Has_Accommodation(username, name, accommodation_id) VALUES (%s, %s, %s, %s)' , username, name, accommodation_id)

			return redirect(url_for('dogHome', user = username, name = name))
		
		except:
			error = 'Add Accommodation Failed. Your dog may already have this accommodation'
			
	return render_template("addAcc.html", error = error, user = username, name = name)


@app.route('/like', methods = ["GET", "POST"])
def like():
	username = request.args.get('user')
	username2 = request.args.get('user2')
	dog2 = request.args.get('dog2')
	error = None
	
	if request.method == "POST":
		username = request.form['user']
		username2 = request.form['user2']
		dog2 = request.form['dog2']
		dog = request.form['dog']
		print(username)
		print(username2)
		print(dog2)
		print(dog)
		try:
			cursor = g.conn.execute('INSERT INTO Likes_Dog(name_likes, name_is_liked_by, username_likes, username_is_liked_by) VALUES (%s, %s, %s, %s)' , dog, dog2 ,username, username2)
			print(username)
			print(username2)
			print(dog2)
			print(dog)
			return redirect(url_for('dogHome2', user = username, user2 = username2, dog2 = dog2))
		
		except:
			error = 'Like failed'
			
	return render_template("like.html", error = error, user = username, user2 = username2, dog2 = dog2)


@app.route('/mydogs')
def mydogs():
    username = request.args.get('user')
    error = None
    names = []
    profile_pictures = []
    try:
        cursor = g.conn.execute('SELECT name, profile_picture FROM Dogs_Owned_By_Has_Physique WHERE username = (%s)', username)
        for result in cursor:
            names.append(result['name'])
            profile_pictures.append(result['profile_picture'])
        cursor.close()
        
        context_names = dict(data_one = names)
        context_profile_pictures = dict(data_two = profile_pictures)
        
    except Exception:
        error = 'Query Failed'
    
    print(username)
    print(context_names)
    print(context_profile_pictures)
   
    return render_template("mydogs.html", error = error, **context_names, **context_profile_pictures, user = username)

@app.route('/dogHome')
def dogHome():
    username = request.args.get('user')
    name = request.args.get('name')
    print(username)
    print(name)
    
    error = None
    birthday_list = []
    breed_list = []
    sex_list = []
    profile_picture_list = []
    bio_list = []
    since_joined_list = []
    size_list = []
    build_list = []
    
    try:
        cursor = g.conn.execute('SELECT birthday, breed, sex, profile_picture, bio, since, size, build FROM Dogs_Owned_By_Has_Physique WHERE username = (%s) AND name = (%s)', username, name)	
        for result in cursor:
          birthday_list.append(str(result['birthday']))
          print(birthday_list)
          breed_list.append(result['breed'])
          sex_list.append(result['sex'])
          profile_picture_list.append(result['profile_picture'])
          bio_list.append(result['bio'])
          since_joined_list.append(result['since'])
          size_list.append(result['size'])
          build_list.append(result['build'])
        cursor.close()
        birthday = str(birthday_list[0])
        print(birthday)
        breed = breed_list[0]
        sex = sex_list[0]
        profile_picture = profile_picture_list[0]
        bio = bio_list[0]
        since_joined = since_joined_list[0]
        size = size_list[0]
        build = build_list[0]
        
    except Exception:
        error = 'Unable to collect dog information'
        
    activity_list = []    
    try:
        cursor = g.conn.execute('SELECT A.description FROM Activities A, Likes_Activity L WHERE L.username = (%s) AND L.name = (%s) AND L.activity_id = A.activity_id', username, name)
        for result in cursor:
            activity_list.append(result['description'])
        cursor.close()
        
        context_activity = dict(data_activities = activity_list)
        
    except Exception:
        error = 'Unable to collect dog activities'    
        
    physique_list = []
    build_list = []
    try:
        cursor = g.conn.execute('SELECT P.size, P.build FROM Physique P, Likes_Physique L WHERE L.username = (%s) AND L.name = (%s) AND L.size = P.size and L.build = P.build', username, name)
        for result in cursor:
            physique_list.append(result['size'])
            build_list.append(result['build'])
        cursor.close()
        print(physique_list)
        context_physiques = dict(data_physiques = physique_list)
        context_builds = dict(data_buils = build_list)
        
    except Exception:
        error = 'Unable to collect dog physiques' 
        
    accomodation_list = []    
    try:
        cursor = g.conn.execute('SELECT A.description FROM Accommodations A, Has_Accommodation H WHERE H.username = (%s) AND H.name = (%s) AND H.accommodation_id = A.accommodation_id', username, name)
        for result in cursor:
            accomodation_list.append(result['description'])
        cursor.close()
        
              
        if len(accomodation_list) == 0:
            accomodation_list.append('None')
            
            
        context_accomodations = dict(data_accomodations = accomodation_list)
        
    except Exception:
        error = 'Unable to collect dog accomodations' 
        
        
    likes_name_list = []
    likes_username_list = []
    try:
        cursor = g.conn.execute('SELECT L.username_is_liked_by, L.name_is_liked_by FROM Likes_Dog L WHERE L.username_likes = (%s) AND L.name_likes = (%s)', username, name)
        for result in cursor:
            likes_name_list.append(result['name_is_liked_by'])
            likes_username_list.append(result['username_is_liked_by'])
        cursor.close()

        context_likes_name = dict(data_likes_name = likes_name_list)
        context_likes_username = dict(data_likes_username = likes_username_list)
        
    except Exception:
        error = 'Unable to collect dog likes' 
            
             

    return render_template("dogHome.html", error = error, user = username, name = name, birthday = birthday, breed = breed, sex = sex, profile_picture = profile_picture, bio = bio, since_joined = since_joined, size = size, build = build, **context_activity, **context_physiques, **context_accomodations, ** context_builds, **context_likes_name, **context_likes_username )


@app.route('/dogHome2')
def dogHome2():
    my_username = request.args.get('user')
    username = request.args.get('user2')
    name = request.args.get('dog2')
    print(username)
    print(name)
    
    error = None
    birthday_list = []
    breed_list = []
    sex_list = []
    profile_picture_list = []
    bio_list = []
    since_joined_list = []
    size_list = []
    build_list = []
    
    try:
        cursor = g.conn.execute('SELECT birthday, breed, sex, profile_picture, bio, since, size, build FROM Dogs_Owned_By_Has_Physique WHERE username = (%s) AND name = (%s)', username, name)
        for result in cursor:
          birthday_list.append(str(result['birthday']))
          breed_list.append(result['breed'])
          sex_list.append(result['sex'])
          profile_picture_list.append(result['profile_picture'])
          bio_list.append(result['bio'])
          since_joined_list.append(result['since'])
          size_list.append(result['size'])
          build_list.append(result['build'])
          
        cursor.close()
        birthday = str(birthday_list[0])
        print(birthday)
        breed = breed_list[0]
        sex = sex_list[0]
        profile_picture = profile_picture_list[0]
        bio = bio_list[0]
        since_joined = since_joined_list[0]
        size = size_list[0]
        build = build_list[0]
        
    except Exception:
        error = 'Unable to collect dog information'
        
    activity_list = []    
    try:
        cursor = g.conn.execute('SELECT A.description FROM Activities A, Likes_Activity L WHERE L.username = (%s) AND L.name = (%s) AND L.activity_id = A.activity_id', username, name)
        for result in cursor:
            activity_list.append(result['description'])
        cursor.close()
        
        context_activity = dict(data_activities = activity_list)
        
    except Exception:
        error = 'Unable to collect dog activities'    
        
    physique_list = []
    build_list = []
    try:
        cursor = g.conn.execute('SELECT P.size, P.build FROM Physique P, Likes_Physique L WHERE L.username = (%s) AND L.name = (%s) AND L.size = P.size and L.build = P.build', username, name)
        for result in cursor:
            physique_list.append(result['size'])
            build_list.append(result['build'])
        cursor.close()
        print(physique_list)
        context_physiques = dict(data_physiques = physique_list)
        context_builds = dict(data_buils = build_list)
        
    except Exception:
        error = 'Unable to collect dog physiques' 
        
    accomodation_list = []    
    try:
        cursor = g.conn.execute('SELECT A.description FROM Accommodations A, Has_Accommodation H WHERE H.username = (%s) AND H.name = (%s) AND H.accommodation_id = A.accommodation_id', username, name)
        for result in cursor:
            accomodation_list.append(result['description'])
        cursor.close()
        
              
        if len(accomodation_list) == 0:
            accomodation_list.append('None')
            
            
        context_accomodations = dict(data_accomodations = accomodation_list)
        
    except Exception:
        error = 'Unable to collect dog accomodations' 
        
        
    likes_name_list = []
    likes_username_list = []
    try:
        cursor = g.conn.execute('SELECT L.username_is_liked_by, L.name_is_liked_by FROM Likes_Dog L WHERE L.username_likes = (%s) AND L.name_likes = (%s)', username, name)
        for result in cursor:
            likes_name_list.append(result['name_is_liked_by'])
            likes_username_list.append(result['username_is_liked_by'])
        cursor.close()

        context_likes_name = dict(data_likes_name = likes_name_list)
        context_likes_username = dict(data_likes_username = likes_username_list)
        
    except Exception:
        error = 'Unable to collect dog likes' 
                

    return render_template("dogHome2.html", error = error, user = my_username, dog2 = name, user2 = username, birthday = birthday, breed = breed, sex = sex, profile_picture = profile_picture, bio = bio, since_joined = since_joined, size = size, build = build, **context_activity, **context_physiques, **context_accomodations, ** context_builds, **context_likes_name, **context_likes_username )

@app.route('/search', methods = ["GET", "POST"])
def search():
    print("hello one")
        
    username = request.args.get('user')
    
    if request.method == "POST":
        print("three")
        username = request.form['user']
        print(username)
        print("four")
        city = request.form['city']
        print("five")
        print("city")
        state = request.form['state']
        size = request.form['size']
        build = request.form['build']
        activity = request.form['activity']
        username_two = request.form['user_two']
        email = request.form['email']
        print(username)
        print(username_two)
        
        return redirect(url_for('addFriend',user = username, city = city, state = state, size = size, build = build, activity = activity, user2 = username_two, email = email))
   
    return render_template("search.html", user = username)
    
@app.route('/addFriend', methods = ["GET", "POST"])
def addFriend():
    username = request.args.get('user')
    print(username)
    city = request.args.get('city')
    state = request.args.get('state')
    print(state)
    size = request.args.get('size')
    build = request.args.get('build')
    #print(size)
    print(build)
    activity = request.args.get('activity')
    username_two = request.args.get('user2')
    email = request.args.get('email')
    error = None
    users_two = []
    names = []
    bios = []
    profile_pictures = []
    
        
    if len(username_two) != 0:
        try:
            cursor = g.conn.execute('SELECT D.username, D.name, D.bio, D.profile_picture FROM Dogs_Owned_By_Has_Physique D WHERE D.username = (%s)', username_two)
            for result in cursor:
                    users_two.append(result['username'])
                    names.append(result['name'])
                    bios.append(result['bio'])
                    profile_pictures.append(result['profile_picture'])
            cursor.close()
                
            context_users_two = dict(data_one = users_two)
            context_names = dict(data_two = names)
            context_profile_pictures = dict(data_three = profile_pictures)
            context_bios = dict(data_four = bios)
        except Exception:
            error = 'Search query failed'
                
    elif len(city) != 0 and len(state) != 0 and len(size) != 0 and len(build) != 0 and len(activity) != 0:
        try:
            cursor = g.conn.execute('SELECT DISTINCT D.username, D.name, D.bio, D.profile_picture FROM Dogs_Owned_By_Has_Physique D, Likes_Activity A, Resides_In R, Address AD, Activities AC WHERE AD.city = (%s) AND AD.state = (%s) AND AD.zip = R.zip AND AD.street_address = R.street_address AND D.username = R.username AND AC.description = (%s) AND AC.activity_id = A.activity_id AND A.username = D.username AND A.name = D.name AND D.size = (%s) AND D.build = (%s)', city, state, activity, size, build)
                
            for result in cursor:
                users_two.append(result['username'])
                names.append(result['name'])
                bios.append(result['bio'])
                profile_pictures.append(result['profile_picture'])
            cursor.close()
                
            context_users_two = dict(data_one = users_two)
            context_names = dict(data_two = names)
            context_profile_pictures = dict(data_three = profile_pictures)
            context_bios = dict(data_four = bios)
                
        except Exception:
            error = 'Search query failed'
                
    elif len(city) != 0 and len(state) != 0 and len(size) != 0 and len(build) != 0:
        try:
            cursor = g.conn.execute('SELECT DISTINCT D.username, D.name, D.bio, D.profile_picture FROM Dogs_Owned_By_Has_Physique D, Resides_In R, Address AD WHERE AD.city = (%s) AND AD.state = (%s) AND AD.zip = R.zip AND AD.street_address = R.street_address AND D.username = R.username AND D.size = (%s) AND D.build = (%s)', city, state, size, build)
                
            for result in cursor:
                users_two.append(result['username'])
                names.append(result['name'])
                bios.append(result['bio'])
                profile_pictures.append(result['profile_picture'])
            cursor.close()
                
            context_users_two = dict(data_one = users_two)
            context_names = dict(data_two = names)
            context_profile_pictures = dict(data_three = profile_pictures)
            context_bios = dict(data_four = bios)
                
        except Exception:
            error = 'Search query failed'
                
                
    elif len(city) != 0 and len(state) != 0 and len(activity) != 0:
        try: 
            cursor = g.conn.execute('SELECT DISTINCT D.username, D.name, D.bio, D.profile_picture FROM Dogs_Owned_By_Has_Physique D, Likes_Activity A, Resides_In R, Address AD, Activities AC WHERE AD.city = (%s) AND AD.state = (%s) AND AD.zip = R.zip AND AD.street_address = R.street_address AND D.username = R.username AND AC.description = (%s) AND AC.activity_id = A.activity_id AND A.username = D.username AND A.name = D.name', city, state, activity)
            for result in cursor:
                users_two.append(result['username'])
                names.append(result['name'])
                bios.append(result['bio'])
                profile_pictures.append(result['profile_picture'])
            cursor.close()
                
            context_users_two = dict(data_one = users_two)
            context_names = dict(data_two = names)
            context_profile_pictures = dict(data_three = profile_pictures)
            context_bios = dict(data_four = bios)
                
        except Exception:
            error = 'Search query failed'
                
                
    elif len(size) != 0 and len(build) != 0 and len(activity) != 0:
        try:
            cursor = g.conn.execute('SELECT DISTINCT D.username, D.name, D.bio, D.profile_picture FROM Dogs_Owned_By_Has_Physique D, Likes_Activity A, Activities AC WHERE AC.description = (%s) AND AC.activity_id = A.activity_id AND A.username = D.username AND A.name = D.name AND D.size = (%s) AND D.build = (%s)', activity, size, build)
            
            for result in cursor:
                users_two.append(result['username'])
                names.append(result['name'])
                bios.append(result['bio'])
                profile_pictures.append(result['profile_picture'])
            cursor.close()
                
            context_users_two = dict(data_one = users_two)
            context_names = dict(data_two = names)
            context_profile_pictures = dict(data_three = profile_pictures)
            context_bios = dict(data_four = bios)
                
        except Exception:
            error = 'Search query failed'
                
                
    elif len(city) != 0 and len(state) != 0:
        try:
            cursor = g.conn.execute('SELECT DISTINCT D.username, D.name, D.bio, D.profile_picture FROM Dogs_Owned_By_Has_Physique D, Resides_In R, Address AD WHERE AD.city = (%s) AND AD.state = (%s) AND AD.zip = R.zip AND AD.street_address = R.street_address AND D.username = R.username', city, state)
            
            for result in cursor:
                users_two.append(result['username'])
                names.append(result['name'])
                bios.append(result['bio'])
                profile_pictures.append(result['profile_picture'])
            cursor.close()
                
            context_users_two = dict(data_one = users_two)
            context_names = dict(data_two = names)
            context_profile_pictures = dict(data_three = profile_pictures)
            context_bios = dict(data_four = bios)
                
        except Exception:
            error = 'Search query failed'
    
                
                
    elif len(size) != 0 and len(build) != 0:
        try:
            cursor = g.conn.execute('SELECT DISTINCT D.username, D.name, D.bio, D.profile_picture FROM Dogs_Owned_By_Has_Physique D WHERE D.size = (%s) AND D.build = (%s)', size, build)
            
            for result in cursor:
                users_two.append(result['username'])
                names.append(result['name'])
                bios.append(result['bio'])
                profile_pictures.append(result['profile_picture'])
            cursor.close()
                
            context_users_two = dict(data_one = users_two)
            context_names = dict(data_two = names)
            context_profile_pictures = dict(data_three = profile_pictures)
            context_bios = dict(data_four = bios)
                
        except Exception:
            error = 'Search query failed'
                
                
    elif len(activity) != 0:
        try:
            print(activity)
            cursor = g.conn.execute('SELECT DISTINCT D.username, D.name, D.bio, D.profile_picture FROM Dogs_Owned_By_Has_Physique D, Likes_Activity A, Activities AC WHERE AC.description = (%s) AND AC.activity_id = A.activity_id AND A.username = D.username AND A.name = D.name', activity)
            
            for result in cursor:
                users_two.append(result['username'])
                names.append(result['name'])
                bios.append(result['bio'])
                profile_pictures.append(result['profile_picture'])
            cursor.close()
                
            context_users_two = dict(data_one = users_two)
            context_names = dict(data_two = names)
            context_profile_pictures = dict(data_three = profile_pictures)
            context_bios = dict(data_four = bios)
                
        except Exception:
            error = 'Search query failed'
                
    elif len(activity) == 0 and len(size) == 0 and len(build) == 0 and len(city) == 0 and len(state) == 0:
        try:
            cursor = g.conn.execute('SELECT DISTINCT D.username, D.name, D.bio, D.profile_picture FROM Dogs_Owned_By_Has_Physique D')
            for result in cursor:
                users_two.append(result['username'])
                names.append(result['name'])
                bios.append(result['bio'])
                profile_pictures.append(result['profile_picture'])
            cursor.close()
                
            context_users_two = dict(data_one = users_two)
            context_names = dict(data_two = names)
            context_profile_pictures = dict(data_three = profile_pictures)
            context_bios = dict(data_four = bios)
                
        except Exception:
            error = 'Search query failed'
    
    else:
        users_two.append('HELLO')
        print(users_two)
        context_users_two = dict(data_one = users_two)
        context_names = dict(data_two = names)
        context_bios = dict(data_four = bios)
        context_profile_pictures = dict(data_three = profile_pictures)
        error = 'Invalid Search. Search by city and state, or by size and build, or by activity'
        
    return render_template("addFriend.html", error = error, user = username, **context_users_two, **context_names, **context_profile_pictures, **context_bios)        

@app.route('/addDog', methods = ["GET", "POST"])
def addDog():
    username = request.args.get('user')
    error = None
    if request.method == "POST":
        username = request.form['user']
        print(username)
        name = request.form['name']
        print(name)
        breed = request.form['breed']
        print(breed)
        birthday = request.form ['birthday']
        print(birthday)
        profile_picture = request.form['profile_picture']
        print(profile_picture)
        bio = request.form['bio']
        print(bio)
        sex = request.form['sex']
        print(sex)
        size = request.form['size']
        print(size)
        build = request.form['build']
        print(build)
        
        try:
            g.conn.execute('INSERT INTO Dogs_Owned_By_Has_Physique(name, breed, birthday, sex, profile_picture, bio, username, size, build) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', name, breed, birthday, sex, profile_picture, bio, username, size, build)
            
        except Exception:
            error = 'Invalid entry. Please note you cannot have two dogs of the same name. Please check your formatting. Inputs may be too long.'
        
                
        if error is None: 
            return redirect(url_for('mydogs',user = username))
            
  
    
    return render_template("addDog.html", error = error, user=username)

    
@app.route('/signup', methods = ["GET", "POST"])
def signup():
    #name = request.form['name']
    #g.conn.execute(
    error = None
    if request.method == "POST":
        username = request.form['username']
        personal_email = request.form['personal_email']
        password = request.form['password']
            
        try:
            g.conn.execute('INSERT INTO Users_Contact_Info_Has_Contact_Info(username, personal_email, password) VALUES (%s, %s, %s)',username, personal_email, password)
        except Exception:
                error = 'Invalid username, email, or password. Check that username and password are at most 15 characters and email is at most 50. Otherwise, username or email is taken. Try again.'
        if error is None:
            return redirect(url_for('signup2',user = username))
            
                
    return render_template("signup.html", error = error)



@app.route('/signup2', methods = ["GET", "POST"])
def signup2():    
    username = request.args.get('user')
    error = None
    if request.method == "POST":
        username = request.form['user']
        name = request.form['name']
        date_joined = request.form['date_joined']
        profile_picture = request.form['profile_picture']
        work_email = request.form['work_email']
        cell_number = request.form['cell_number']
        home_number = request.form['home_number']
        work_number = request.form['work_number']
        street_address = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zip']
	will_host = request.form['will_host']
	will_travel = request.form['will_travel']
	mile_radius = request.form['mile_radius']
	will_carpool = request.form['will_carpool']
	has_kids = request.form['has_kids']
	has_pets = request.form['has_pets']
	has_back = request.form['has_back']
	allows_dropoffs = request.form['allows_dropoffs']
	
        
        if error is None and name:
            try: 
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET name = (%s) WHERE username = (%s)',name, username)
            except Exception:
                error = 'Invalid name. Name must be 25 characters or less. Try again'
        if error is None and date_joined:
            try: 
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET date_joined = (%s) WHERE username = (%s)',date_joined, username)
            except Exception:
                error = 'Invalid date. Try again'
        if error is None and profile_picture:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET profile_picture = (%s) WHERE username = (%s)', profile_picture, username)
            except Exception:
                error = 'Invalid profile_picture URL. URL must be 200 characters or less. Try again'           
        if error is None and work_email:
            try: 
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET work_email = (%s) WHERE username = (%s)',work_email, username)
            except Exception:
                error = 'Invalid email. Email must be less than 50 characters and a valid address Try again'
        if error is None and cell_number:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET cell_number = (%s) WHERE username = (%s)',cell_number, username)
            except Exception:
                error = 'Invalid cell number. Number mmust be 11 characters or less and must be unique. Try again'
        if error is None and home_number:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET home_number = (%s) WHERE username = (%s)',home_number, username)
            except Exception:
                error = 'Invalid home number. Number mmust be 11 characters or less and must be unique. Try again'
        if error is None and work_number:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET work_number = (%s) WHERE username = (%s)', work_number, username)
            except Exception:
                error = 'Invalid work number. Number must be 11 characters or less and must be unique. Try again'
        if error is None and (will_host == 'Y'):
            try:
                g.conn.execute('INSERT INTO Will_Host(username, has_backyard, has_children, has_other_pets, allows_dropoffs) VALUES (%s, %s, %s, %s)', username, has_back, has_kids, has_pets, allows_dropoffs)
            except Exception:
                error = 'Invalid will host'
        if error is None and (will_travel == 'Y'):
            try:
                g.conn.execute('INSERT INTO Will_Travel(username,will_carpool, mile_radius) VALUES (%s, %s, %s)', username, will_carpool, mile_radius)
            except Exception:
                error = 'Invalid will host'
        if error is None:   
            address = []
            try:
                cursor = g.conn.execute('SELECT street_address FROM Address WHERE street_address = (%s) AND zip = (%s)', street_address, zipcode)
                for result in cursor:
                    address.append(result['street_address'])
                cursor.close()
            except Exception:
                error = 'Unable to query address'
            if len(address) == 0:
                try:
                    g.conn.execute('INSERT INTO Address(street_address, city, state, zip) VALUES (%s, %s, %s, %s)', street_address, city, state, zipcode)
                except Exception:
                    error = 'Invalid street address, city, state, or zipcode. Address is at most 30 characters while city is at most 20 and state is at most 15. Zipcode must be an integer'
        if error is None:
            try:
                g.conn.execute('INSERT INTO Resides_In(username, street_address, zip) VALUES (%s, %s, %s)', username, street_address, zipcode)
            except Exception:
                error = 'Unable to create address'
        if error is None:
            return redirect(url_for('home',user = username))



            
                
    return render_template("signup2.html", error = error, user=username) 
        
        

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """ 

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
