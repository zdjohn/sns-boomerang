from sns_boomerang.handlers import job_stream_handler
from sns_boomerang.common.items import Job, Topic, TopicSubscriptions


def mocked_due(parsed):
    return True


def mocked_added(parsed):
    return True


def mock_pass_or_none(*args, **kwargs):
    pass


def test_job_added(monkeypatch):

    def mock_topic_get(topic, check_is_active):
        assert check_is_active == True
        assert topic == 'mock-topic'
        topic = Topic(topic, arn='mocked-arn')
        monkeypatch.setattr(topic, 'add_or_update', mock_pass_or_none)
        return topic

    job_new = {'Records': [{'eventName': 'INSERT',
                            'dynamodb': {'NewImage': {'id': {'S': 'mock-id'}, 'topic': {'S': 'mock-topic'}}}}]}
    monkeypatch.setattr(Topic, 'get', mock_topic_get)
    log = job_stream_handler.handle_stream(job_new)
    assert log['INSERT'] == 1
    assert log['REMOVE'] == 0


def test_job_added_empty_topic(monkeypatch):
    job_new = {'Records': [{'eventName': 'INSERT',
                            'dynamodb': {'NewImage': {'id': {'S': 'mock-id'}, 'topic': {'S': 'mock-topic'}}}}]}
    monkeypatch.setattr(Topic, 'get', mock_pass_or_none)
    log = job_stream_handler.handle_stream(job_new)
    assert log['INSERT'] == 0
    assert log['REMOVE'] == 0


def test_job_due(monkeypatch):

    def mock_parse(cls, record):
        job = Job('mock-topic', 'payload', 123)
        monkeypatch.setattr(job, 'is_valid', True)
        monkeypatch.setattr(job, 'publish', mock_pass_or_none)
        return job

    job_due = {'Records': [{'eventName': 'REMOVE',
                            'dynamodb': {
                                'OldImage': {
                                    'id': {'S': 'mock-id'},
                                    'is_valid': {'N': 1}
                                }
                            }
                            }]}

    monkeypatch.setattr(job_stream_handler, '_parse_record', mock_parse)
    log = job_stream_handler.handle_stream(job_due)
    assert log['INSERT'] == 0
    assert log['REMOVE'] == 1


def test_job_due_empty(monkeypatch):

    def mock_parse(cls, record):
        return None

    job_due = {'Records': [{'eventName': 'REMOVE',
                            'dynamodb': {}
                            }]}

    monkeypatch.setattr(job_stream_handler, '_parse_record', mock_parse)
    log = job_stream_handler.handle_stream(job_due)
    assert log['INSERT'] == 0
    assert log['REMOVE'] == 0
