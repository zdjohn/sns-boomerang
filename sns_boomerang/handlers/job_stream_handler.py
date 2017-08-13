from sns_boomerang.common.items import *
from enum import Enum


class UpdateType(Enum):
    REMOVE = 'REMOVE'
    MODIFY = 'MODIFY'
    INSERT = 'INSERT'


class RecordImageType(Enum):
    NEW = 'NewImage'
    OLD = 'OldImage'


def handle(update):
    """
    parsing dynamo db update events batch
    :param update: {'Records':[...]}
    :return: None
    """
    events = update.get('Records', [])
    for event in events:
        if UpdateType.INSERT.value == event.get('eventName'):
            _handle_job_added(_parse_record(event, RecordImageType.NEW.value))
        if UpdateType.REMOVE.value == event.get('eventName'):
            _handle_job_due(_parse_record(event, RecordImageType.OLD.value))


def _parse_record(stream_record, record_image_type=RecordImageType.NEW.value):
    """
    parsing job payload from dynamo db image
    :param record:
    :param record_image_type:
    :return: Job
    """
    job_record = stream_record.get('dynamodb', {}).get(record_image_type)
    job = Job.get_by_stream_record(job_record)
    return job


def _handle_job_added(added_job):
    """
    check if job topic is already created
    create topic in sns, update topic arn table
    :param added_job:
    :return: None
    """
    topic = Topic.get(added_job.topic, check_is_active=True)
    if topic:
        topic.add_or_update()


def _handle_job_due(job):
    """publish job with its payload"""
    if job.is_valid:
        job.publish()