from sns_boomerang.common.items import Job, Topic, TopicSubscriptions
from enum import Enum


class UpdateType(Enum):
    REMOVE = 'REMOVE'
    MODIFY = 'MODIFY'
    INSERT = 'INSERT'


class RecordImageType(Enum):
    NEW = 'NewImage'
    OLD = 'OldImage'


def _handle_job_added(event):
    """
    check if job topic is already created
    create topic in sns, update topic arn table
    :param added_job:
    :return: None
    """
    added_job = _parse_record(event, RecordImageType.NEW.value)
    topic = Topic.get(added_job.topic, check_is_active=True)
    if topic:
        topic.add_or_update()
        return True
    return False


def _handle_job_due(event):
    """publish job with its payload"""
    job = _parse_record(event, RecordImageType.OLD.value)
    if job and job.is_valid:
        job.publish()
        return True
    return False


def _parse_record(stream_record, record_image_type=RecordImageType.NEW.value):
    """
    parsing job payload from dynamo db image
    :param record:
    :param record_image_type:
    :return: Job
    """
    job_record = stream_record.get('dynamodb', {}).get(record_image_type)
    job = Job.from_stream_record(job_record)
    return job


def handle_stream(update):
    """
    parsing dynamo db update events batch
    :param update: {'Records':[...]}
    :return: None
    """
    handler_mapping = {
        UpdateType.INSERT.value: _handle_job_added,
        UpdateType.REMOVE.value: _handle_job_due
    }

    events = update.get('Records', [])
    event_processed = {'INSERT': 0, 'REMOVE': 0}
    for event in events:
        if event.get('eventName') != UpdateType.MODIFY.value and handler_mapping[event.get('eventName')](event):
            event_processed[event.get('eventName')] += 1
    return event_processed
