# Tasks Helper
> Spring 2022. Written in Python3 using Flask, HTML, Bootstrap, and Jinja. Database management through SQLAlchemy and SQLite.

## Project Overview
A Flask web application using Python3 and HTML that allows users to create, modify, and delete tasks while simulating user authentication (login, logout, and registration). 

### Features
* Web pages rendered with Jinja templating and styled with Bootstrap.
* Account information and event details stored into a relational SQLite database.
* Database records managed using SQLAlchemy and HTTP requests.

## Table of Contents
* [Application Requirements](https://github.com/jschhie/tasks-helper/#application-requirements)
* [Visual Demo](https://github.com/jschhie/tasks-helper/#visual-demo)


## Application Requirements
This web app requires ```Python3```, as well as the following packages: ```flask```, ```flask-login```, and ```flask-sqlalchemy```.

### How to Run the App
To run this application, first download this repository and the packages mentioned above.

(Assuming in Terminal) First, enter:
```bash 
git clone https://github.com/jschhie/tasks-helper.git [folderNameHere]
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
At start up, users may toggle the nagivation bar to switch between the Account Login and Registration Pages. Signed in/newly registered users will be greeted with their personal Home Page, which displays all tasks and possible actions to manage them (update, create, delete).

## Visual Demo
todo
