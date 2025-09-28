from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)


# GET /messages
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages])


# POST /messages
@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    new_msg = Message(
        body=data.get("body"),
        username=data.get("username")
    )
    db.session.add(new_msg)
    db.session.commit()
    return jsonify(new_msg.to_dict()), 201


# PATCH /messages/<id>
@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    data = request.get_json()
    msg = Message.query.get_or_404(id)
    if "body" in data:
        msg.body = data["body"]
    db.session.commit()
    return jsonify(msg.to_dict())


# DELETE /messages/<id>
@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
