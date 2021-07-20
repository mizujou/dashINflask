from blog import db, login_manager
from blog import bcrypt
from flask_login import UserMixin # Check info of the class: F12. Mixin provide the methode neccessary for Falsk to make Login work.

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=60), nullable=False, unique=True) 
    password_hash = db.Column(db.String(length=60), nullable=False) # Flask will hash the passwords with 60 characters
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship("Item", backref="owned_user", lazy=True) # lazy allow SQL alchemy to reach all the items at once

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        # This funtion is here to check if the User has enough money to purchase an item. False or True --> go through the if statement
        return self.budget >= item_obj.price 

    def can_sell(self, item_obj):
        # This function checks if the item is owned by the user
        return item_obj in self.items

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey("user.id")) # The foreign key create the link between the two class / SQL Tables

    def __repr__(self):
        return f"Item {self.name}"

    def buy(self, user):
        # Updates the budget of a user after purchasing an Item
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        # Updates the budget of a user after selling an Item
        self.owner = None
        user.budget += self.price
        db.session.commit()

    