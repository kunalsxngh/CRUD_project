from application import app, db
from application.models import Reviews, Games, Recommendations
from application.forms import ReviewForm, GameForm
from flask import Flask, render_template, request, redirect, url_for

@app.route("/")
@app.route("/home")
def home():
    all_reviews = Reviews.query.all()
    return render_template("home.html", all_reviews = all_reviews)

@app.route("/create", methods=["GET", "POST"])
def create():
    form = ReviewForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_review = Reviews(
                author=form.author.data,
                body=form.body.data,
                rating=form.rating.data
            )
            db.session.add(new_review)
            db.session.commit()
            return  redirect(url_for("home"))
    
    return render_template('add.html', title="Create a task", form = form)


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form = ReviewForm()
    review = Reviews.query.filter_by(id=id).first()
    if request.method == "POST":
        review.body = form.body.data
        revoew.rating = form.body.rating
        db.session.commit()
        return  redirect(url_for("home"))
    return render_template("update.html", form=form, title="Update Review", review = review)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    review = Reviews.query.filter_by(id=id).first()
    db.session.delete(review)
    db.session.commit()
    return  redirect(url_for("home"))

@app.route("/addgame", methods=["GET", "POST"])
def addgame():
    form = GameForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_game = Games(
                name = form.name.data,
                genre = form.genre.data
            )
            db.session.add(new_game)
            db.session.commit()
            return  redirect(url_for("home"))
    return render_template('addgame.html', title="Add a game", form = form)
