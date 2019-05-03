from sns_boomerang.handlers import ttl_enforcer
from sns_boomerang.common.items import Job


def mock_flush():
    pass


def test_flush(monkeypatch):
    monkeypatch.setattr(Job, 'flush', mock_flush)
    assert ttl_enforcer.flush()
