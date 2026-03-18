import os
import time
import pytest

import utils


def test_parse_interval_various():
    assert utils.parse_interval('3600') == 3600
    assert utils.parse_interval('5s') == 5
    assert utils.parse_interval('2m') == 120
    assert utils.parse_interval('1h') == 3600
    assert utils.parse_interval('1d') == 86400


def test_parse_interval_invalid():
    with pytest.raises(ValueError):
        utils.parse_interval('nope')


def test_get_env_variable(monkeypatch):
    monkeypatch.delenv('FOO', raising=False)
    assert utils.get_env_variable('FOO', 'bar') == 'bar'
    monkeypatch.setenv('FOO', 'baz')
    assert utils.get_env_variable('FOO', 'bar') == 'baz'


def test_set_timezone_from_env(monkeypatch):
    # Ensure TZ not set, and default is applied
    monkeypatch.delenv('TZ', raising=False)
    utils.set_timezone_from_env(default='UTC')
    assert os.environ.get('TZ') == 'UTC'

    # When tzset raises, function should silently handle it
    monkeypatch.setenv('TZ', 'Europe/Paris')
    # force time.tzset to raise AttributeError (some platforms may not have it)
    monkeypatch.setattr(time, 'tzset', lambda: (_ for _ in ()).throw(AttributeError()), raising=False)
    # call should not raise
    utils.set_timezone_from_env(default='UTC')
