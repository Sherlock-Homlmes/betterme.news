# libraries
import pytest


@pytest.mark.asyncio
async def test_get_self_fail_because_not_logged_in(client):
    """
    INPUT:
        Call self api
    OUTPUT:
        Error not authenticated
    """
    response = client.get("/api/auth/self")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_oauth_link(client):
    """
    INPUT:
        Call oauth link api
    OUTPUT:
        Get discord link
    """
    response = client.get("/api/auth/oauth-link")
    assert response.status_code == 200
    assert (
        response.json()["discord_link"] == "https://discord.com/api/oauth2/xxxxxxxxxxxxxxxxxxxxxx"
    )
