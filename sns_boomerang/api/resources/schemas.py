from flask_restplus import fields

"""
requests
"""
def job_request_model():
    return {
        'id': fields.String(description='The job unique identifier'),
        'payload': fields.String(required=True, description='json string payload'),
        'time_due': fields.Float(required=True, description='time due for scheduled job'),
        'version': fields.Integer(default=1, description='job version'),
        'is_valid': fields.Integer(default=1, description='either 1 or 0'),
        'time_scheduled': fields.Float
    }


"""
topic response
"""
