import subprocess
import logging

import docker_cleanup


def test_prune_images_success(monkeypatch, caplog):
    class Result:
        stdout = "ok"
        stderr = ""

    def fake_run(args, check, capture_output, text):
        assert args[0:3] == ['docker', 'image', 'prune']
        return Result()

    monkeypatch.setattr(subprocess, 'run', fake_run)
    caplog.set_level(logging.INFO)
    docker_cleanup.prune_images('24h')
    assert 'Image prune completed successfully.' in caplog.text or 'Pruning images older than 24h' in caplog.text


def test_prune_images_called_with_filter(monkeypatch):
    calls = {}

    def fake_run(args, check, capture_output, text):
        calls['args'] = args
        return type('R', (), {'stdout': '', 'stderr': ''})()

    monkeypatch.setattr(subprocess, 'run', fake_run)
    docker_cleanup.prune_images('48h')
    assert any('--filter=until=48h' == a or '--filter=until=48h' in a for a in calls['args'])


def test_prune_images_handles_file_not_found(monkeypatch):
    def fake_run(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(subprocess, 'run', fake_run)
    # should not raise
    docker_cleanup.prune_images('24h')
