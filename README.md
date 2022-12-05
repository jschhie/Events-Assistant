# Events Assistant 🗓 

> Python, HTML, SQLite, Bootstrap, Flask, Jinja.

## Project Overview
A dynamic Flask web application using Python3 and HTML that allows users to create, modify, search, and delete custom events while handling user authentication (login, logout, and registration). 

### Features
* Web pages rendered with Jinja templating and styled with Bootstrap elements.
* Account information and event details stored into a relational SQLite database.
* Database records managed using SQLAlchemy and HTTP requests.

## Table of Contents
* [Application Requirements](https://github.com/jschhie/Events-Assistant/#application-requirements)
* [Visual Demo](https://github.com/jschhie/Events-Assistant/#visual-demo)


## Application Requirements
The packages and libraries needed to run this web app are listed in the ```requirements.txt``` file. 
The following command will install all the required Python packages:
```bash
pip3 install -r requirements.txt
```

### How to Run the App
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
At start up, users may toggle the nagivation bar to switch between the Account Login and Registration Pages. Signed in/newly registered users will be greeted with their personal Home Page.

## Visual Demo
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/new%20register.png" alt="Registration Page" style="width:70%">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/new%20login.png" alt="Login Page" style="width:70%">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/new%20home.png" alt="Home Page with tasks" style="width:70%">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/new%20create.png" alt="Create Event" style="width:70%">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/new%20update.png" alt="Update Events" style="width:70%">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/new%20search.png" alt="Search Events" style="width:70%">
