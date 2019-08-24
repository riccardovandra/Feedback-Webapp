from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__) #initialize the app

#define database location

ENV = 'prod'

#used for running two databases, a development one and a production one
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2458@localhost/Lexus' #dev database
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://boluiftsgcyjiq:098e1fd62f21bbcdd662bd1e12e9e0729c56a8e3c94f6667cad03485bb201346@ec2-54-83-201-84.compute-1.amazonaws.com:5432/d2ue09khl27p66' #production database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# define the database
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        print(customer,dealer,rating,comments) 
        #simple validation
        if customer == '' or dealer == '':
            return render_template('index.html',message='Please enter required fields')
        # check if the customer already exists
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer,dealer,rating,comments)
            db.session.add(data) #add the data to the database
            db.session.commit()
            send_mail(customer,dealer,rating,comments)
            return render_template('success.html')
        return render_template('index.html',message='You already submitted feedback')


if __name__ == '__main__':
    app.run()