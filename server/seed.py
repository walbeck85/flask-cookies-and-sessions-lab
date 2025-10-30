#!/usr/bin/env python3
"""
Run this script from the project root:
    python -m server.seed
Or from the server directory:
    python seed.py
This will populate the SQLite database with fake users and articles.
"""

from random import randint
from faker import Faker

# Fix: Changed `from server.app import app` to `from app import app`
from app import app
# Fix: Changed `from server.models import ...` to `from models import ...`
from models import db, Article, User

fake = Faker()

def main():
    with app.app_context():
        print("Deleting all records...")
        Article.query.delete()
        User.query.delete()

        print("Creating users...")
        users = [User(name=fake.name()) for _ in range(25)]
        db.session.add_all(users)

        print("Creating articles...")
        articles = []
        for i in range(100):
            content = fake.paragraph(nb_sentences=8)
            preview = content[:25] + '...'
            article = Article(
                author=fake.name(),
                title=fake.sentence(),
                content=content,
                preview=preview,
                minutes_to_read=randint(1, 20),
            )
            article.user = users[i // 4]
            articles.append(article)

        db.session.add_all(articles)
        db.session.commit()
        print("Complete.")

if __name__ == "__main__":
    main()
