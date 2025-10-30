#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
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
    """
    Step 3: Return article data or paywall message based on session['page_views'].
    """

    # Initialize and increment the page view count
    session['page_views'] = session.get('page_views', 0) + 1
    session.modified = True

    # Enforce the 3-article paywall limit
    if session['page_views'] <= 3:
        article = Article.query.get(id)

        if not article:
            return jsonify({'message': 'Article not found'}), 404

        article_data = ArticleSchema().dump(article)
        return jsonify(article_data), 200

    else:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401


if __name__ == '__main__':
    app.run(port=5555)
