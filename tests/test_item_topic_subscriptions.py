from sns_boomerang.common.items import sns_client, sns_resource, Topic, TopicSubscriptions, TOPIC_TABLE
import pytest
from .conftest import sub_mock, test_topic, test_topic_arn, test_subscibers_list, test_sub_arn, test_protocol, test_endpoint


def test_get_subscriptions_by_topic(monkeypatch, setup_topic_resource):
    subs = TopicSubscriptions(test_topic)
    assert subs.topic


def test_list_subscribers(monkeypatch, setup_topic_resource):
    subs = TopicSubscriptions(test_topic)
    assert subs.lists() == test_subscibers_list


def test_remove_subscriber_from_topic(monkeypatch, setup_topic_resource):
    subs = TopicSubscriptions(test_topic)
    assert subs.remove(test_sub_arn)
    assert sub_mock.is_deleted


def test_add_subscribe_to_topic(monkeypatch, setup_topic_resource):
    subs = TopicSubscriptions(test_topic)
    assert subs.add(test_protocol, test_endpoint)
