from flask import Flask, request, make_response, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    body = data.get('body')
    username = data.get('username')
    
    if not body or not username:
        return abort(400, description="Both 'body' and 'username' are required")
    
    message = Message(body=body, username=username)
    db.session.add(message)
    db.session.commit()
    
    return jsonify(message.to_dict()), 201

# Route to update a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id) 
    data = request.get_json()
    
    body = data.get('body')
    if body:
        message.body = body
        db.session.commit()
    
    return jsonify(message.to_dict())

# Route to delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id) 
    db.session.delete(message)
    db.session.commit()
    
    return jsonify({"message": "Message deleted successfully"}), 200

if __name__ == '__main__':
    app.run(port=5555)
