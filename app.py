# Dependencies 
import scrape_mars # (our scrape_mars.py)
from flask_pymongo import PyMongo
from flask import Flask, redirect, render_template 


# Create an instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def index(): 

    # Find data
    mars_dict = mongo.db.mars_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars_data = scrape_mars.initialize_browser()
    
    mars_data = scrape_mars.pandas_scrape_facts()
    mars_data = scrape_mars.browser_scrape_news()
    mars_data = scrape_mars.browser_scrape_image()
    mars_data = scrape_mars.browser_scrape_weather()
    mars_data = scrape_mars.browser_scrape_hemispheres()
    
    mongo.db.mars_dict.update({}, mars_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__": 
    app.run(debug= True)

