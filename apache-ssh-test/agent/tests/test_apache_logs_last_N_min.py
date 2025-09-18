import os
from datetime import datetime, timedelta
import pytest

def get_recent_apache_errors(ssh_client, minutes: int):
    """
    Reads Apache error log entries from the last `minutes` via SSH.
    """
    time_threshold = datetime.now() - timedelta(minutes=minutes)

    cmd = "cat /var/log/apache2/error.log"
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    lines = stdout.readlines()

    recent_errors = []

    for line in lines:
        if line.startswith("["):
            try:
                timestamp_str = line[1:26]  # '[Mon Sep 15 22:26:48 2025]'
                timestamp = datetime.strptime(timestamp_str, "%a %b %d %H:%M:%S %Y")
                if timestamp >= time_threshold:
                    recent_errors.append(line.strip())
            except Exception:
                continue

    return recent_errors

@pytest.mark.apache
def test_no_recent_apache_errors(ssh_client):
    """
    Checks that there are no Apache errors in the last LOG_CHECK_MINUTES.
    """
    log_check_minutes = int(os.getenv("LOG_CHECK_MINUTES", 5))
    errors = get_recent_apache_errors(ssh_client, log_check_minutes)

    assert not errors, (
        f"Apache errors detected in the last {log_check_minutes} minutes:\n" +
        "\n".join(errors)
    )

