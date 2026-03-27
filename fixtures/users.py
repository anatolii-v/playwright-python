import pytest
import uuid
from test_data.users import EXISTING_USER

@pytest.fixture
def new_user():
    return {
        "name": "John Doe",
        "email": f"john_{uuid.uuid4().hex}@test.com",
        "password": "123456JohnDoe",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": ("1", "2", "2008"),
        "address": "Magic Street 10",
        "country": "United States",
        "state": "NY",
        "city": "NY",
        "zip": "1010",
        "mobile": "123456789",
    }

@pytest.fixture
def existing_user():
    return EXISTING_USER.copy()
