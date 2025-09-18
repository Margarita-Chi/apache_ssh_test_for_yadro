import pytest
import allure

@pytest.mark.apache
def test_apache_service_active(ssh_client):
    """
    Verify that the apache2 process is running in the target container.
    """
    with allure.step("Check running processes for apache2"):
        stdin, stdout, stderr = ssh_client.exec_command("pgrep -fl apache2")
        processes = stdout.read().decode().strip()

    with allure.step("Verify apache2 process exists"):
        assert processes, "apache2 process not found — web server is not running"

