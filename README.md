# Tasks Helper
> Spring 2022. Written in Python3 using Flask, HTML, Bootstrap, and Jinja. Database management through SQLAlchemy and SQLite.

## Project Overview
A Flask web application using Python3 and HTML that allows users to create, modify, and delete tasks through HTTP requests while simulating login, logout, and registration features. 
Stylized and rendered web pages using Jinja templating and Bootstrap.
Managed account information and event details using SQLAclhemy and stored records into a SQLite database.

## Application Requirements
This web app requires ```Python3```, as well as the following packages: ```flask```, ```flask-login```, and ```flask-sqlalchemy```.

### How to Run the App
To run this application, first download this repository and the packages mentioned above.

(Assuming in Terminal) First, enter:
```bash 
git clone https://github.com/jschhie/tasks-helper.git [folderNameHere]
```
> where ```folderNameHere``` can be any name to store the project source code.

Next, go into the folder: 
```bash 
cd [folderNameHere]
```

Finally, enter:
```bash
python3 main.py
```

> This initializes an empty database (```tasks_database.db```) and creates and activates the Flask web app. 

The user can then access and interact with the application at http://127.0.0.1:5000/ via any web browser. 
At start up, the user will be greeted with the Login Page and may click the nagivation bar to toggle the menu.
