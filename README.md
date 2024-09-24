# Dashboard Builder 📅 

> Flask, Python, HTML, CSS, JavaScript, SQLAlchemy, Jinja, Bootstrap.

## Overview
* A Flask web app with a user-friendly dashboard for custom events. 
* Features include:
  * Create, modify, delete, bookmark, group, and un/hide events
  * User authentication (login, logout, registration) and filtered search functionality
  * Uses a relational SQLite database for data management
  * HTML templates rendered using Jinja, with a styled interface built using CSS, JavaScript, and Bootstrap
* Hosted on PythonAnywhere at: https://jschhie.pythonanywhere.com. 

## Table of Contents
* [Demo](https://github.com/jschhie/Events-Assistant/#visual-demo)
* [Running the App Manually](https://github.com/jschhie/Events-Assistant/#running-the-app-manually)

## Visual Demo
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/allgroups.png" alt="Home Page with All Groups">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/onegroup.png" alt="Home Page with Math Homework Group and side bar menu">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/update-group.png" alt="Update Events">

## Running the App Manually
1. Clone this repository:
```bash 
git clone https://github.com/jschhie/events-assistant.git [folderNameHere]
```

2. Navigate into the folder:
```bash 
cd [folderNameHere]
```

3. Install the required packages:
```bash
pip3 install -r requirements.txt
```
4. Run the Flask app:
```bash
python3 main.py
```

<p>User can access the web application at: http://127.0.0.1:5000/ via any web browser.</p>
