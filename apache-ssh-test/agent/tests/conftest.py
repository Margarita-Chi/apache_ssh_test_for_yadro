import os
import pytest
import paramiko
from paramiko.ssh_exception import SSHException, NoValidConnectionsError
import allure

def pytest_configure(config):
    """
    Register custom markers for pytest.
    """
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "apache: mark test as apache-related"
    )

@pytest.fixture(scope="session")
def target_host():
    """
    Return the hostname of the target container. Default is 'target'.
    """
    return os.getenv("TARGET_HOST", "target")

@pytest.fixture(scope="session")
def ssh_client(target_host):
    """
    Create an SSH client connected to the target host.
    The client is closed automatically after the session.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    with allure.step(f"Connect to SSH on {target_host}"):
        try:
            client.connect(
                hostname=target_host,
                username=os.getenv("SSH_USER", "tester"),
                password=os.getenv("SSH_PASSWORD", "testerpass"),
                port=int(os.getenv("SSH_PORT", 22)),
                timeout=5,
                look_for_keys=False,
                allow_agent=False
            )
        except (SSHException, NoValidConnectionsError, OSError) as exc:
            pytest.skip(f"Could not connect via SSH to {target_host}: {exc}")
    
    yield client

    with allure.step(f"Close SSH connection to {target_host}"):
        client.close()

