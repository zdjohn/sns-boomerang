from flask_restplus import fields


def job_request_model():
    """

    :return:
    """
    return {
        'id': fields.String(description='The job unique identifier'),
        'payload': fields.String(required=True, description='json string payload'),
        'time_due': fields.Float(required=True, description='time due for scheduled job'),
        'version': fields.Integer(default=1, description='job version'),
        'is_valid': fields.Integer(default=1, description='either 1 or 0'),
        'time_scheduled': fields.Float
    }


def subscriber_request_model():
    """

    :return:
    """
    return {
        'endpoint': fields.String(requied=True, description='lambda arn or https endpoints')
    }


"""
topic_resource response
"""
