import pytest
import os
import requests
import allure

@pytest.mark.apache
def test_apache_404(target_host):
    """
    Verify that the server correctly returns 404 for non-existent pages.
    """
    url = f"http://{target_host}/nonexistent_page.html"

    with allure.step(f"Send GET request to {url}"):
        response = requests.get(url, timeout=5)

    with allure.step("Verify response status code is 404"):
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    expected_text = os.getenv("EXPECTED_404_TEXT")
    with allure.step("Verify 404 page content"):
        if expected_text:
            assert expected_text in response.text, (
                f"404 page does not contain expected text: '{expected_text}'"
            )
        else:
            default_texts = ["Not Found", "Apache", "404"]
            assert any(text in response.text for text in default_texts), \
                "404 page does not contain expected text"

