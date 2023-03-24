# Events Assistant

> Flask, Python, HTML, CSS, SQLite, Bootstrap, Jinja, JavaScript.

## Project Overview
A dynamic Flask web application that allows users to create, modify, search, and delete custom events while handling user authentication (login, logout, and registration). Extra features: bookmarking important events and un/hiding completed ones.

This web app is hosted on <a href="https://www.pythonanywhere.com/">PythonAnywhere</a>. You can visit this project at https://jschhie.pythonanywhere.com/login?next=%2F. 

### Features
* Web pages rendered with Jinja templating and styled with CSS and Bootstrap elements.
* Account information and event details stored into a relational SQLite database.

## Table of Contents
* [Application Requirements](https://github.com/jschhie/Events-Assistant/#application-requirements)
* [Visual Demo](https://github.com/jschhie/Events-Assistant/#visual-demo)

## Application Requirements
The packages and libraries needed to run this web app are listed in the ```requirements.txt``` file. 
The following command will install all the required Python packages:
```bash
pip3 install -r requirements.txt
```

### Running the App: Manually
To run this application manually, first download this repository and the packages listed above.

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

The user can then access and interact with the web app at http://127.0.0.1:5000/ via any web browser. 

## Visual Demo
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/css%20register2.png" alt="Registration Page">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/css%20login2.png" alt="Login Page">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/css%20home2.png" alt="Home Page with tasks">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/css%20update2.png" alt="Update Events">
