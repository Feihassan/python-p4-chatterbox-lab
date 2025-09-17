from app import app, db
from models import Message

with app.app_context():
    # Clear existing
    Message.query.delete()

    # Add seed messages
    m1 = Message(body="Hello World!", username="Alice")
    m2 = Message(body="This is my first post!", username="Bob")

    db.session.add_all([m1, m2])
    db.session.commit()

    print("✅ Seeded database with messages!")
