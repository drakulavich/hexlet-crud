# imports
import os
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

# get the folder where this file runs
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = 'articles.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import models


@app.route('/')
def index():
    """
    Searches the database for articles, then displays them.
    """

    articles = db.session.query(models.Article)
    return render_template('index.html', articles=articles)


@app.route('/add', methods=['POST'])
def add_article():
    """
    Add new post to database.
    """

    new_article = models.Article(request.form['name'], request.form['body'])
    db.session.add(new_article)
    db.session.commit()

    flash('New entry was successfully created')
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_article(post_id):
    """
    Deletes post from database.
    """

    db.session.query(models.Article).filter_by(post_id=post_id).delete()
    db.session.commit()
    flash('The entry was deleted.')
    return redirect(url_for('index'))


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_article(post_id):

    if request.method == 'POST':
        # update record
        update_article = db.session.query(models.Article).get(post_id)
        update_article.name = request.form['name']
        update_article.body = request.form['body']
        db.session.commit()

        flash('The entry was successfully updated')
        return redirect(url_for('index'))

    # open page for editing
    article = db.session.query(models.Article).get(post_id)
    return render_template('edit.html', article=article)


if __name__ == '__main__':
    app.run()
