import sys
from datetime import date

from flask import Flask, abort, request
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.DateTime(dt_format='iso8601')
}

parser.add_argument(
    'date',
    type=inputs.date,
    help='The event date with the correct format is required! The correct format is YYYY-MM-DD!',
    required=True
)

parser.add_argument(
    'event',
    type=str,
    help='The event name is required!',
    required=True
)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


class TodayEventsResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return Event.query.filter(Event.date == date.today()).all()


class EventByID(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        event = Event.query.filter(Event.id == id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return event

    def delete(self, id):
        event = Event.query.filter(Event.id == id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        Event.query.filter_by(id=id).delete()
        db.session.commit()
        return {"message": "The event has been deleted!"}


class EventResource(Resource):
    def post(self):
        args = parser.parse_args()
        event = f"{args['event']}"
        date = args['date'].date()

        new_event = Event(event=event, date=date)
        db.session.add(new_event)
        db.session.commit()

        res = {
            "message": "The event has been added!",
            "event": f"{args['event']}",
            "date": f"{args['date'].date()}"
        }
        return res

    @marshal_with(resource_fields)
    def get(self):
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        if start_time and end_time:
            events = Event.query.filter(Event.date >= start_time).\
                filter(Event.date <= end_time).all()
            if len(events) < 1:
                abort(404, {"message": "The event doesn't exist!"})
            return events
        return Event.query.all()


api.add_resource(TodayEventsResource, '/event/today')
api.add_resource(EventResource, '/event')
api.add_resource(EventByID, '/event/<int:id>')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
