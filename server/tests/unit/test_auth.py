# libraries
import pytest


@pytest.mark.asyncio
async def test_get_self_fail_because_not_logged_in(client):
    """
    INPUT:
        Get self api
    OUTPUT:
        Error not logged in
    """
    response = client.get("/api/auth/self")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"
