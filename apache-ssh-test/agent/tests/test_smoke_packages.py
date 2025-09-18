import pytest
import allure

@pytest.mark.smoke
@allure.feature("Smoke Commands")
@allure.story("tar command")
@allure.severity(allure.severity_level.CRITICAL)
def test_tar_command(ssh_client):
    '''
    Smoke test for tar command
    '''
    with allure.step("Create a temporary directory and file"):
        # Create directory and a test file inside
        ssh_client.exec_command("mkdir -p /tmp/tar_test && echo 'hello' > /tmp/tar_test/file.txt")
    
    with allure.step("Archive the directory using tar"):
        # Create a tar archive of the temporary directory
        ssh_client.exec_command("tar -cf /tmp/tar_test.tar -C /tmp tar_test")
    
    with allure.step("Verify the contents of the archive"):
        # List the contents of the archive
        stdin, stdout, stderr = ssh_client.exec_command("tar -tf /tmp/tar_test.tar")
        files = stdout.read().decode()
        # Attach the archive contents to Allure report
        allure.attach(files, name="archive_content", attachment_type=allure.attachment_type.TEXT)
        assert "tar_test/file.txt" in files, "tar failed to create the expected archive"
    
    with allure.step("Clean up temporary files"):
        ssh_client.exec_command("rm -rf /tmp/tar_test /tmp/tar_test.tar")


@pytest.mark.smoke
@allure.feature("Smoke Commands")
@allure.story("ln command")
@allure.severity(allure.severity_level.CRITICAL)
def test_ln_command(ssh_client):
    '''
    Smoke test for ln command
    '''
    with allure.step("Create a temporary file"):
        ssh_client.exec_command("echo 'test' > /tmp/test_ln_file")
    
    with allure.step("Create a symbolic link"):
        ssh_client.exec_command("ln -s /tmp/test_ln_file /tmp/test_ln_link")
    
    with allure.step("Verify the content through the symbolic link"):
        stdin, stdout, stderr = ssh_client.exec_command("cat /tmp/test_ln_link")
        content = stdout.read().decode().strip()
        # Attach the file content to Allure report
        allure.attach(content, name="linked_file_content", attachment_type=allure.attachment_type.TEXT)
        assert content == "test", "ln failed to create a working symbolic link"
    
    with allure.step("Clean up temporary files"):
        ssh_client.exec_command("rm -f /tmp/test_ln_file /tmp/test_ln_link")

