#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
# Fix: Changed `from server.models import ...` to `from models import ...`
from models import db, Article, User, ArticleSchema, UserSchema

def create_app():
    app = Flask(__name__)
    app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # Updated path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    db.init_app(app)
    migrate = Migrate(app, db)

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
        # This logic was already correct and meets all requirements.
        session['page_views'] = session.get('page_views', 0) + 1
        session.modified = True

        if session['page_views'] <= 3:
            article = Article.query.get(id)
            if not article:
                return jsonify({'message': 'Article not found'}), 404
            article_data = ArticleSchema().dump(article)
            return jsonify(article_data), 200
        else:
            return jsonify({'message': 'Maximum pageview limit reached'}), 401

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'articles' not in inspector.get_table_names():
            print(".  Detected missing 'articles' table. Run these commands from server directory:")
            print("   flask db upgrade && python seed.py")

    app.run(port=5555)
