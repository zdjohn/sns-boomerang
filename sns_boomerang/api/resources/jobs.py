from flask_restplus import Resource, Namespace
from sns_boomerang.common.items import Job
from .schemas import *

ns = Namespace('jobs', description='schedule job')

job = ns.model('Job', model=job_request_model())


@ns.route('/<string:id>')
@ns.param('id', 'job id')
class Jobs(Resource):
    @staticmethod
    def get(id):
        """
        get job by id
        :param id: job id
        :return:
        """
        job_item = Job.get(id)
        if job_item:
            return job_item.__dict__, 200
        return 404
