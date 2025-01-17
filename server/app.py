from flask import Flask, request, make_response, jsonify
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

def create_default_message():
    with app.app_context():
        if Message.query.count() == 0:  # Check if any messages exist
            default_message = Message(body="Hello 👋", username="Liza")
            db.session.add(default_message)
            db.session.commit()

# Call the function to create a default message
create_default_message()

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        return make_response([message.to_dict() for message in messages], 200)
    
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(message)
        db.session.commit()
        return make_response(message.to_dict(), 201)
def test_updates_body_of_message_in_database(self):
    '''updates the body of a message in the database.'''
    with app.app_context():
        m = Message.query.first()
        if m is None:
            m = Message(body="Hello 👋", username="Liza")
            db.session.add(m)
            db.session.commit()

        id = m.id
        # Now proceed to update the message

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if message is None:
        return make_response({'error': 'Message not found'}, 404)

    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
        db.session.commit()
        return make_response(message.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response({'deleted': True}, 200)

if __name__ == '__main__':
    app.run(port=5555)
