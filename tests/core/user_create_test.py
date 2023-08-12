import pytest
from core.models import User

@pytest.mark.django_db
def test_user_create(client):
    user = User.objects.create_user(username="abc",
                                    first_name="abc",
                                    last_name="abc",
                                    email="abc@gmail.com",
                                    password="1234567qw",
                                    )

    expected_response = {
                          "username": "string245",
                          "first_name": "string1",
                          "last_name": "string",
                          "email": "user@example.com"
                        }
    response = client.get(f"/core/profile")
    assert response.status_code == 200
    assert expected_response == response
