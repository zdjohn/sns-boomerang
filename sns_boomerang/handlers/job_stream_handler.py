from sns_boomerang.common.items import Job, Topic
from enum import Enum


class UpdateType(Enum):
    REMOVE = 'REMOVE'
    MODIFY = 'MODIFY'
    INSERT = 'INSERT'


class RecordImageType(Enum):
    NEW = 'NewImage'
    OLD = 'OldImage'


def _handle_job_added(events):
    new_jobs = [_parse_record(event, RecordImageType.NEW.value) for event in events
                if (event.get('eventName') == UpdateType.INSERT.value)]
    new_topic_count = 0
    for topic_name in set([job.topic for job in new_jobs]):
        topic = Topic.get(topic_name, check_is_active=False)
        if not topic:
            new_topic = Topic(topic_name)
            new_topic.add_or_update()
            new_topic_count += 1

    return len(new_jobs), new_topic_count


def _handle_job_due(events):
    """publish job with its payload"""
    total_job_precessed = 0
    due_events = [events for event in events
                  if (event.get('eventName') == UpdateType.REMOVE.value)]
    for event in due_events:
        job = _parse_record(event, RecordImageType.OLD.value)
        if job and job.is_valid:
            job.publish()
            total_job_precessed += 1
    return total_job_precessed


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

    events = update.get('Records', [])
    event_processed = {'INSERT': 0, 'REMOVE': 0, 'TOPIC_NEW': 0}

    # handle new jobs
    inserted, new_topic = _handle_job_added(events)

    event_processed['INSERT'] = inserted
    event_processed['TOPIC_NEW'] = new_topic

    # handle job due
    event_processed['REMOVE'] = _handle_job_due(events)

    return event_processed
