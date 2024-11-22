# Dashboard Builder 📅 

> Flask, Python, HTML, CSS, JavaScript, SQLAlchemy, Jinja, Bootstrap.

## Project Overview
A Flask web app that provides a user-friendly, multi-functional, and collaborative dashboard for custom events. 

This web app is hosted on <a href="https://www.pythonanywhere.com/">PythonAnywhere</a>. You can visit this project at https://jschhie.pythonanywhere.com. 

### Features
* Allows users to create, modify, delete, bookmark, group, un/hide events, and add group members/share any group of tasks
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
<img src="https://github.com/jschhie/Events-Assistant/blob/master/demos/update-group.png" alt="Updating Task as Group Member">
