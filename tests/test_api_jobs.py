from sns_boomerang.api.resources.jobs import Jobs
from sns_boomerang.common.items import Job
import pytest
from werkzeug.exceptions import NotFound


def test_get_job(monkeypatch):
    test_id = 'test-id'

    def mock_get(id):
        assert id == test_id
        return Job('topic', 'payload', 123, id=test_id)

    monkeypatch.setattr(Job, 'get', mock_get)
    response = Jobs.get(test_id)
    assert response[0]['id'] == test_id
    assert response[1] == 200


def test_get_no_job(monkeypatch):
    test_id = 'test-id'

    def mock_get(id):
        assert id == test_id
        return None

    monkeypatch.setattr(Job, 'get', mock_get)
    with pytest.raises(NotFound):
        Jobs.get(test_id)
