# Dashboard Builder 📅 

> Flask, Python, HTML, CSS, JavaScript, SQLAlchemy, Jinja, Bootstrap.

## Project Overview
A Flask web app that provides a user-friendly, multi-functional dashboard for custom events. 

This web app is hosted on <a href="https://www.pythonanywhere.com/">PythonAnywhere</a>. You can visit this project at https://jschhie.pythonanywhere.com. 

### Features
* Allows users to create, modify, delete, bookmark, group, and un/hide events
* Handles user authentication (login, logout, registration) and filtered searches with a relational SQLite database
* HTML templates rendered with Jinja and styled interface with CSS, JavaScript, and Bootstrap framework

## Table of Contents
* [Demo](https://github.com/jschhie/Events-Assistant/#visual-demo)
* [Running the App Manually](https://github.com/jschhie/Events-Assistant/#running-the-app-manually)

## Running the App Manually
### Application Requirements
To run this application manually (via your ```localhost```), download the required packages and this repository, as described below.

The packages and libraries needed to run this web app are listed in the ```requirements.txt``` file. 
The following command will install all the required packages:

```bash
pip3 install -r requirements.txt
```
(Assuming in Terminal) First, enter:

<hr>

Next, to clone this repository, enter:
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

The user can then access and interact with the web app at http://127.0.0.1:5000/ via any web browser. 

## Visual Demo
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/home-all.png" alt="Home Page with all tasks">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/home-spanish.png" alt="Home Page with Spanish Homework Group">

<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/update-group.png" alt="Update Events">
