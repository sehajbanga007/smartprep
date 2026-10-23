import pytest


@pytest.mark.api
def test_home_page_serves_website(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"SmartPrep" in response.content
