#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
# We will use the original relative path, which works when
# all commands are run from inside the /server directory.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

@app.route('/articles/<int:id>')
def show_article(id):
    # This is the completed logic for the lab
    
    # Step 1 & 2: Initialize and Increment Session
    session['page_views'] = session.get('page_views', 0) + 1
    session.modified = True # Ensure the session is saved even if the value is just read

    # Step 3: Send Response Based on Session
    if session['page_views'] <= 3:
        article = Article.query.get(id)
        if not article:
            return jsonify({'message': 'Article not found'}), 404
        article_data = ArticleSchema().dump(article)
        return jsonify(article_data), 200
    else:
        # User has viewed more than 3 pages
        return jsonify({'message': 'Maximum pageview limit reached'}), 401


if __name__ == '__main__':
    app.run(port=5555)

