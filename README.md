# Task Dashboard 📅 

> Flask, Python, HTML, CSS, JavaScript, SQLAlchemy, Jinja, Bootstrap.


## Project Overview
A Flask web app that provides a user-friendly, multi-functional, and collaborative dashboard for custom events. 

This web app is hosted on <a href="https://www.pythonanywhere.com/">PythonAnywhere</a>. You can visit this project at https://jschhie.pythonanywhere.com. 

### Features
* Allows users to create, modify, delete, bookmark, group, un/hide events, and add group members/share any group of tasks
* Handles user authentication (login, logout, registration) and filtered searches with a relational SQLite database
* HTML templates rendered with Jinja and styled interface with CSS, JavaScript, and Bootstrap framework

## Overview
* A Flask web app with a user-friendly dashboard for custom, schedulable tasks. 
* Features include:
  * Create, modify, delete, bookmark, group, and un/hide tasks
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

The user can then access and interact with the web app at http://127.0.0.1:5000/ via any web browser. 

## Visual Demo
### Home Page with All Groups
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/init-lisa-group.png" alt="Home Page with All Groups">

### Share Group: Add Members
> Here, lisa123 is the owner of this group
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/share-group.png" alt="Share Group / Add Members">

### Group Member View -- with Editor Access Mode
> ryan123 is a member of lisa123's group with editor access mode 
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/ryan-group-member-view.png" alt="Group Member View: with Editor Access Mode">

### Updating Task as a Group Member
> ryan123's updates to tasks in lisa123's shared group will be reflected for everyone in that group
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/group-member-edit.png" alt="Updating Task as Group Member">