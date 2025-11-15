import os
from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from datetime import datetime

_client = None
_db = None

def get_mongo_uri():
    # Default local replica-set-friendly URI (user can override)
    return os.environ.get('MONGO_URI', 'mongodb://localhost:27017')

def connect():
    global _client, _db
    if _client:
        return _db

    uri = get_mongo_uri()
    _client = MongoClient(uri)
    _db = _client.get_database(os.environ.get('MONGO_DB', 'lineup'))

    # Ensure indexes
    _db.timeslots.create_index([('start_ts', 1)])
    _db.bookings.create_index([('timeslot_id', 1)])
    _db.bookings.create_index([('status', 1)])

    return _db

def get_db():
    if not _db:
        return connect()
    return _db

def create_timeslot(start_ts, end_ts, capacity=1, label=None):
    db = get_db()
    doc = {
        'start_ts': start_ts,
        'end_ts': end_ts,
        'capacity': int(capacity),
        'label': label,
        'booked_count': 0,
        'is_active': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    res = db.timeslots.insert_one(doc)
    doc['_id'] = res.inserted_id
    return doc

def list_timeslots(filter_query=None):
    db = get_db()
    q = filter_query or {'is_active': True}
    docs = list(db.timeslots.find(q))
    return docs

def get_timeslot(timeslot_id):
    from bson import ObjectId
    db = get_db()
    return db.timeslots.find_one({'_id': ObjectId(timeslot_id)})

def book_timeslot(timeslot_id, name, contact=None):
    """
    Attempt to create a booking for given timeslot_id.
    Uses transactions when available (replica set). Returns booking doc on success.
    Raises RuntimeError on full or PyMongoError on DB issues.
    """
    from bson import ObjectId
    db = get_db()
    client = _client

    # Use session/transaction if available (requires replica set)
    try:
        if client is not None and client.start_session:
            with client.start_session() as session:
                with session.start_transaction(write_concern=WriteConcern(w='majority')):
                    ts = db.timeslots.find_one({'_id': ObjectId(timeslot_id)}, session=session)
                    if not ts or not ts.get('is_active', True):
                        raise RuntimeError('Timeslot not found or inactive')
                    if ts.get('booked_count', 0) >= ts.get('capacity', 1):
                        raise RuntimeError('Timeslot full')
                    booking = {
                        'timeslot_id': ObjectId(timeslot_id),
                        'name': name,
                        'contact': contact,
                        'status': 'booked',
                        'created_at': datetime.utcnow(),
                    }
                    res = db.bookings.insert_one(booking, session=session)
                    db.timeslots.update_one({'_id': ObjectId(timeslot_id)}, {'$inc': {'booked_count': 1}, '$set': {'updated_at': datetime.utcnow()}}, session=session)
                    booking['_id'] = res.inserted_id
                    return booking
        else:
            # Fallback non-transactional (possible race conditions on heavy concurrency)
            ts = db.timeslots.find_one({'_id': ObjectId(timeslot_id)})
            if not ts or not ts.get('is_active', True):
                raise RuntimeError('Timeslot not found or inactive')
            if ts.get('booked_count', 0) >= ts.get('capacity', 1):
                raise RuntimeError('Timeslot full')
            booking = {
                'timeslot_id': ObjectId(timeslot_id),
                'name': name,
                'contact': contact,
                'status': 'booked',
                'created_at': datetime.utcnow(),
            }
            res = db.bookings.insert_one(booking)
            db.timeslots.update_one({'_id': ObjectId(timeslot_id)}, {'$inc': {'booked_count': 1}, '$set': {'updated_at': datetime.utcnow()}})
            booking['_id'] = res.inserted_id
            return booking
    except PyMongoError as e:
        raise
