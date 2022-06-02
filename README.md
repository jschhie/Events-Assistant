# Events Assistant
> Written in Python3 using Flask, HTML, Bootstrap, and Jinja. Database management through SQLAlchemy and SQLite.

## Project Overview
A dynamic Flask web application using Python3 and HTML that allows users to create, modify, search, and delete schedulable and trackable events while handling user authentication (login, logout, and registration). 

Deployed on Heroku: https://events-assistant-app.herokuapp.com/

### Features
* Web pages rendered with Jinja templating and styled with Bootstrap.
* Account information and event details stored into a relational SQLite database.
* Database records managed using SQLAlchemy and HTTP requests.

## Table of Contents
* [Application Requirements](https://github.com/jschhie/Events-Assistant/#application-requirements)
* [Visual Demo](https://github.com/jschhie/Events-Assistant/#visual-demo)


## Application Requirements
You can access the website at https://events-assistant-app.herokuapp.com/, or you can also download this GitHub repository to access the source code.

The packages and libraries needed to run this web app are listed in the ```requirements.txt``` file. 
The following command will install all the required Python packages:
```bash
pip3 install -r requirements.txt
```

### How to Run the App (Manually)
To run this application, first download this repository and the packages mentioned above.

(Assuming in Terminal) First, enter:
```bash 
git clone https://github.com/jschhie/events-assistant.git [folderNameHere]
```

Next, go into the folder: 
```bash 
cd [folderNameHere]
```

Finally, enter:
```bash
python3 main.py
```

> Above command will create and activate the Flask web app with an empty database (```tasks_database.db```). 

The user can then access and interact with the application at http://127.0.0.1:5000/ via any web browser. 
At start up, users may toggle the nagivation bar to switch between the Account Login and Registration Pages. Signed in/newly registered users will be greeted with their personal Home Page, which displays all events and CRUD (create, read, update, and delete) operations to manage them.

## Visual Demo
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/Register.png" alt="Registration Page" style="width:70%">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/Login.png" alt="Login Page" style="width:70%">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/Home%20Search.png" alt="Home Page with tasks" style="width:70%">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/Create.png" alt="Create Event" style="width:70%">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/Update.png" alt="Update Events" style="width:70%">
