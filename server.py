
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
        
                  
    return render_template("home.html", user = username, name = name, profile_picture = profile_picture)

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
            birthday_list.append(result['birthday'])                            
            breed_list.append(result['breed'])
            sex_list.append(result['sex'])
            profile_picture_list.append(result['profile_picture'])
            bio_list.append(result['bio'])
            since_joined_list.append(result['since'])
            size_list.append(result['size'])
            build_list.append(result['build'])
        cursor.close()
        birthday = birthday_list[0]
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
    try:
        cursor = g.conn.execute('SELECT P.size, P.build FROM Physique P, Likes_Physique L WHERE L.username = (%s) AND L.name = (%s) AND L.size = P.size and L.build = P.build', username, name)
        for result in cursor:
            physique_list.append(result['size', 'build'])
        cursor.close()
        
        context_physiques = dict(data_physiques = physique_list)
        
    except Exception:
        error = 'Unable to collect dog physiques' 
        
    accomodation_list = []    
    try:
        cursor = g.conn.execute('SELECT A.description FROM Accommodations A, Has_Accommodation H WHERE H.username = (%s) AND H.name = (%s) AND H.accomodation_id = A.accomodation_id', username, name)
        for result in cursor:
            accomodation_list.append(result['description'])
        cursor.close()
        
        context_accomodations = dict(data_accomodations = accomodation_list)
        
    except Exception:
        error = 'Unable to collect dog accomodations' 
            
             

    return render_template("dogHome.html", error = error, user = username, name = name, birhday = birthday, breed = breed, sex = sex, profile_picture = profile_picture, bio = bio, since_joined = since_joined, size = size, build = build, **context_activity, **context_physiques, **context_accomodations)


@app.route('/addDog', methods = ["GET", "POST"])
def addDog():
    username = request.args.get('user')
    error = None
    if request.method == "POST":
        name = request.form['name']
        breed = request.form['breed']
        birthday = request.form ['birthday']
        profile_picture = request.form['profile_picture']
        bio = request.form['bio']
        sex = request.form['sex']
        size = request.form['size']
        build = request.form['build']
        weight_low = request.form['weight_low']
        weight_high = request.form['weight_high']
        
        try:
            g.conn.execute('INSERT INTO Dogs_Owned_By_Has_Physique(username, name) VALUES (%s, %s)', username, name)
        except Exception:
            error = 'Invalid name. Name should be at most 11 characters and you cannot have two dogs of the same name'
        
        if error is None and breed:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET breed = (%s) WHERE username = (%s) AND name = (%s)', breed, username,name)
            except Exception:
                error = 'Invalid breed. Number mmust be 11 characters or less. Try again'
        if error is None and birthday:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET birthday = ({:%B %d, %Y}) WHERE username = (%s) AND name = (%s)', birthday, username,name)
            except Exception:
                error = 'Invalid breed. Number mmust be 11 characters or less. Try again'
        if error is None and profile_picture:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET profile_picture = (%s) WHERE username = (%s) AND name = (%s)', profile_picture, username,name)
            except Exception:
                error = 'Invalid birthday. Number mmust be 11 characters or less. Try again'
        if error is None and profile_picture:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET profile_picture = (%s) WHERE username = (%s) AND name = (%s)', profile_picture, username,name)
            except Exception:
                error = 'Invalid birthday. Number mmust be 11 characters or less. Try again'
        if error is None and bio:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET bio = (%s) WHERE username = (%s) AND name = (%s)', bio, username,name)
            except Exception:
                error = 'Invalid bio. Number mmust be 50 characters or less. Try again'
        if error is None and sex:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET sex = (%s) WHERE username = (%s) AND name = (%s)', sex, username,name)
            except Exception:
                error = 'Invalid sex. Number mmust be 50 characters or less. Try again'
        if error is None and size:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET size = (%s) WHERE username = (%s) AND name = (%s)', size, username,name)
            except Exception:
                error = 'Invalid size. Number mmust be 50 characters or less. Try again'
        if error is None and build:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET build = (%s) WHERE username = (%s) AND name = (%s)', build, username,name)
            except Exception:
                error = 'Invalid size. Number mmust be 50 characters or less. Try again'
        
        login = []
        try: 
            cursor = g.conn.execute('SELECT * FROM Physique WHERE size = (%s) AND build = (%s) AND weight_low = (%d) AND weight_high = (%d)', size, build, weight_low, weight_high)
            for result in cursor:
                login.append(result['*'])  # can also be accessed using result[0]
            cursor.close()
        except Exception:
            error = 'Invalid search query'
        if len(login) != 1:
            error = 'Invalid range'
        
        
        if error is None and weight_low:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET weight_low = (%d) WHERE username = (%s) AND name = (%s)', weight_low,size, username,name)
            except Exception:
                error = 'Invalid weight_low. Number mmust be 50 characters or less. Try again'
        if error is None and weight_high:
            try:
                g.conn.execute('UPDATE Users_Contact_Info_Has_Contact_Info SET weight_high = (%d) WHERE username = (%s) AND name = (%s)', weight_high,size, username,name)
            except Exception:
                error = 'Invalid weight_high. Number mmust be 50 characters or less. Try again'
                
        if error is None: 
            return redirect(url_for('mydogs',user = username))
            
  
    
    return render_template("addDog.html")

    
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
            g.conn.execute('INSERT INTO Users_Contact_Info_Has_Contact_Info(username, personal_email, password) VALUES (%s, %s)',username, personal_email, password)
        except Exception:
                error = 'Invalid username, email, or password. Check that username and password are at most 15 characters and email is at most 50. Otherwise, username or email is taken. Try again.'
        if error is None:
            return redirect(url_for('signup2',user = username))
            
                
    return render_template("signup.html", error = error)



@app.route('/signup2', methods = ["GET", "POST"])
def signup2():    
    username = request.args.get('username')
    error = None
    
    if request.method == "POST":
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
        zip = request.form['zip']
        
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
                error = 'Invalid work number. Number mmust be 11 characters or less and must be unique. Try again'
        if error is None:
            address = []
            try:
                cursor = g.conn.execute('SELECT street_address FROM Address WHERE street_address = (%s) AND zip = (%s)', street_address, zip)
                for result in cursor:
                    address.append(result['street_address'])
                cursor.close()
            except Exception:
                error = 'Unable to query address'
            if len(address) == 0:
                try:
                    g.conn.execute('INSERT INTO Address(street_address, city, state, zip) VALUES (%s, %s, %s, %s)', street_address, zip)
                except Exception:
                    error = 'Invalid street address, city, state, or zipcode. Address is at most 30 characters while city is at most 20 and state is at most 15. Zipcode must be an integer'
        if error is None:
            try:
                g.conn.execute('INSERT INTO Resides_In(username, street_address, zip) VALUES (%s, %s, %s)', username, street_address, zip)
            except Exception:
                error = 'Unable to create address'
        if error is None:
            return redirect(url_for('home',user = username))      
            
                
    return render_template("signup2.html", error = error) 
        
        

'''
# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
'''

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
