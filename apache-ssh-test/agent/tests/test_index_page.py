import os
import requests
import pytest

@pytest.mark.apache
def test_index_page(target_host):
    """
    Checks that /index.html is accessible and contains the expected text if defined.
    """
    url = f"http://{target_host}/index.html"
    response = requests.get(url, timeout=5)

    # Verify HTTP status
    assert response.status_code == 200, f"/index.html is not accessible, received status {response.status_code}"

    # Verify page content if EXPECTED_INDEX_TEXT is set
    expected_text = os.getenv("EXPECTED_INDEX_TEXT")
    if expected_text:
        assert expected_text in response.text, (
            f"/index.html does not contain the expected text: '{expected_text}'"
        )

