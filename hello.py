from flask import Flask
from flask import request
from flask import render_template
from pymongo import MongoClient
import pandas as pd
import re

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.toucantech
collection = db.development


def insert(first_name,last_name,email_address,school):
	collection.insert_one({'first_name': first_name,
								'last_name':last_name,
								'email_address': email_address,
								'school': school})
	

@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    new_first_name = request.form['first_name'].title()
    new_last_name = request.form['last_name'].title()
    new_email = request.form['email']
    new_school = request.form['school'].title()
 
    #Regular expressions for names and email from Stack overflow
    regex = re.compile(r'^[A-Z]\w+(?:\s[A-Z]\w+?)?\s(?:[A-Z]\w+?)?$')
    email_check = re.compile(r'[^@]+@[^@]+\.[^@]+')

    if re.match(regex,new_first_name + " " + new_last_name) and re.match(regex,new_school) \
    and re.match(email_check,new_email):
    
        insert(new_first_name,new_last_name,new_email,new_school)
    
        people_in_school = []
        if collection.find({"school": new_school}).count() > 1:
            for post in collection.find({"school": new_school}):
                post.pop('_id', None)
                people_in_school.append(post)
        
        df = pd.DataFrame(people_in_school)
       
    
    
        concated = "Thanks for joining %d other people using ToucanTech!" \
        %(collection.count() - 1)
    
        return render_template("submit-form.html", people_in_school = people_in_school, concated = concated,\
        	html_table= df.to_html())

    else:
    	return "Please try again" + render_template("my-form.html") 

if __name__ == '__main__':
    app.run()