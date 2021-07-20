# My First App Shared on GitHub

This app is more or less the fruit of 2, 3 different tutorials. I just modified the code to fit my needs into another app with the same architecture as this one. This one will be a mockup trial that will be uploaded onto my GitHub.

> I did test the app before uploading in it onto GitHub and it was working. But you will have to use a virtual environment or having the librairies that I am using in this project like Flask, flask_login, dash, sqlalchemy, etc, ...

## The Resources that I used:

* The Flask app, [YouTube Video found on freeCodeCamp](https://www.youtube.com/watch?v=Qr4QMBUPxWo&t=6689s) by JimShapedCoding

* For only the Dash app, I learned a lot from that [YouTube Channel](https://www.youtube.com/channel/UCqBFsuAz41sqWcFjZkqmJqQ) by Charming Data

* For the missing link between Flask and Dash, it wasn't that easy to found. I found a lot of help in an article written by [Oleg Komarov and his GitHub](https://github.com/okomarov/dash_on_flask)

Oleg is actually the person I sent an email too and pushed me to publish an issue onto his app to find some help. Big Thanks to him.

## My Goal

My Goal for this app is to get some help. I am myself only a Junior Dev AI, I know that this app can be improved in many ways, but, for today, I want to focus onto one issue that I have.

We now have a structure with one Flask app that we are using for a good quality login, something that the free version of Dash is lacking.

And we also have a Dash app inside of the Flask app showing some Graphs.

**What I would like to learn:**

I learned from one of the tutorial to create a path between the Flask app and the Dash app, but then, when I am inside the Dash app, I can't come back to the Flask app. I would like to know if it is possible to do it. And learn how to do it.


## 1. Process to launch an Flask APP

```
$ set FLASK_APP=app.py
$ flask run
```

Now, instead of closing the app and launch it again everytime you make some changes, you can turn on the `debug mode`

$ set FLASK_DEBUG=1 (Except that it didn't work for me...)

---

## 2. His database

This is a little app, running locally so he isn't planning on linking it with a database. But this is this part that I will have later to look into and link in the backend the app with a database using Flask and mySQL or mongo ...

I guess we could keep a little database type SQLite3 for our web app since it is only going to keep in memory not sensible parameters

Yet, he is going to use SQLite3 so it might be useful. First, we will install some additionnal tools

```
$ pip install flask-sqlalchemy
```

---

## 3. Database

nullable to have allow empty fields

unique to make sure to note have the same username twice in the database for example. Very important for primary keys in databases.

```python
from blog import db

db.create_all() # Creates all the tables within our python file

from blog import Item # To import the Table
#Then, you can create an exemple in the Table
item1 = Item(name="iPhoneX", price=799, barcode="89756521589", description="desc")
db.session.add(item1) # These two lines are a little similar to github, add the Item just created, and commit to register it onto our db
db.session.commit()
```

db.drop_all() can delete all the data in the database, even the tables
db.create_all() can recreates the tables that we already created, but not the data in them

item1 = Item.query.filter_by(name="iPhone 10")

Assign an owner to wn item must be done by specifying the id of the owner

```python
item1.owner = User.query.filter_by(username="John").first()
db.session.rollback() # because the line above was a mistake a we can fix it with this command)
item1.owner = User.query.filter_by(username="John").first().id

# Filtering:
i = Item.filter_by(name='iPhone10')
i.owned_user

```

---

## 4. Flask Form Template

$ pip install flask-wtf
$ pip install wtforms # <-- Will show that everything is already installed

We reuse our base.html template, but there is a difference. We need to have a secure key because, with this form, Users will be interacting with our databases. Do generate a secure key:

```python
import os
os.urandom(12).hex()
```

--> 

Added `{{ form.hidden_tag() }}` on the register.html file to secure the page.

$ pip install email_validator

---

## 5. Display error messages

We can do that by using a built-in function again, Flash.

`&times;` is the X symbole to close a window in a html file

---

## 6. Store Crypted Passwords

$ pip install flask_bcrypt

## 7. Manage Login System

$ pip install flask-login

The flask_login method has a lot of function pre-built like accessing the current user (see base.html current_user)


## 8. Differentiate Users

Take down a page if they aren't logged in. For that, we will use the funtion `login_required`

---

## home.html first version

````
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">

    <title>HomePage</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
        <a class="navbar-brand" href="#">Mizujou Flask App</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav mr-auto">
              <li class="nav-item active">
                  <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
              </li>
              <li class="nav-item">
                  <a class="nav-link" href="#">Blog</a>
              </li>
          </ul>
          <ul class="navbar-nav">
              <li class="nav-item">
                  <a class="nav-link" href="#">Login</a>
              </li>
              <li class="nav-item">
                  <a class="nav-link" href="#">Register</a>
              </li>
          </ul>
        </div>
    </nav>

    <h1>Here is the Home Page, Welcome!</h1>

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js" integrity="sha384-SR1sx49pcuLnqZUnnPwx6FCym0wLsk5JZuNx2bPPENzswTNFaQU1RDvt3wT4gWFG" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.min.js" integrity="sha384-j0CNLUeiqtyaRmlzUHCPZ+Gy5fQu0dQ6eZ/xAww941Ai1SxSY+0EQqNXNE6DZiVc" crossorigin="anonymous"></script>
    -->
  </body>
  <style>
    body {
      background-color: #212121;
      color: white;
    }
  </style>
</html>
```