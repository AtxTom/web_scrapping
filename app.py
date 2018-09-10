# import necessary libraries
# flask is the framework
# "Flask"  the prototype used to create instances of web application(s) 
from flask import Flask, render_template, redirect

#  flask_pymongo is the framework
#  PyMongo is used to create instances
from flask_pymongo import PyMongo

import scrape_info

"""
Create instance of Flask app
When we import Flask, we need to create an instance of the Flask class for our web app. That’s what line 19 does.
 __name__ is a special variable that gets as value the string "__main__" Therefore, __name__ will be equal to "__main__" at the end.
That means the if conditional statement is satisfied and the app.run() method will be executed. 
This technique allows the programmer to have control over script’s behavior."""

app = Flask(__name__)

"""Use flask_pymongo to set up mongo connection
 The following is the standard URI connection scheme for your local machine.
 mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
 See the documentation here: https://docs.mongodb.com/manual/reference/connection-string/
 mongodb:// A required prefix to identify that this is a string in the standard connection format.
  localhost: is the server address to connect to. It identifies either a hostname, IP address, or UNIX domain socket.
  27017 is the port  /weather_app is the database. """

app.config["MONGO_URI"] = "mongodb://localhost:27017/weather_app"

# PyMongo connects to the MongoDB server running on port 27017 on localhost, 
# to the database named weather_app. This database is exposed as the db attribute that can be used in line 46.
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    # This will fetch all of the forecasts from mongo 
    # and the other code passes that to the flask Templating engine to generate html with that data.
    #  "collection" is your table but you can also name that table, like you did in the craigslist activity, "listings".
    forecasts = mongo.db.collection.find()
    

    # return template and data
    # With the templating, whatever you use on the left of the assignment in "forecasts=forecasts" as the parameter,
    #  will be the name of the data inside of the html file. 
    # You could say data=forecasts, and use data inside the html file.
    return render_template("index.html", forecasts=forecasts)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    #  Setting a variable to the scrape_info python file and calling the function "scrape_weather() or "scrape_surf".
    weather = scrape_info.scrape_weather()
    surf = scrape_info.scrape_surf()

    # Store results into a dictionary
    forecast = {
        "time": weather["time"],
        "location": weather["name"],
        "min_temp": weather["min_temp"],
        "max_temp": weather["max_temp"],
        "surf_location": surf["location"],
        "height": surf["height"],
    }

    # Insert forecast into database
    mongo.db.collection.insert_one(forecast)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
