import string
from datetime import date

import pytest
import requests
from hypothesis import given, settings, strategies as st, HealthCheck

BASE_URL = "http://localhost:8000"

TEST_USERNAME = "fuzz_test_user"
TEST_PASSWORD = "fuzz_test_password_123"


@pytest.fixture(scope="module")
def session():
    s = requests.Session()

    s.post(f"{BASE_URL}/auth/register", data={
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    })

    login_response = s.post(f"{BASE_URL}/auth/login", data={
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    })

    assert login_response.status_code == 200
    return s


random_name = st.text(min_size=0, max_size=300)

random_number = st.one_of(
    st.floats(min_value=-1e9, max_value=1e9, allow_nan=False, allow_infinity=False),
    st.integers(min_value=-1_000_000, max_value=1_000_000),
)

random_date_string = st.one_of(
    st.dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31)).map(str),
    st.text(alphabet=string.printable, min_size=0, max_size=20),
)


def is_valid_name(name: object) -> bool:
    return (
        isinstance(name, str)
        and 1 <= len(name) <= 100
        and name.isprintable()
    )


@settings(
    max_examples=200,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
    deadline=None,
)
@given(
    name=random_name,
    proteins=random_number,
    fats=random_number,
    carbs=random_number,
    calories=random_number,
)
def test_fuzz_create_entry_invalid_values(session, name, proteins, fats, carbs, calories):
    payload = {
        "name": name,
        "proteins": proteins,
        "fats": fats,
        "carbs": carbs,
        "calories": calories,
        "entry_date": str(date.today()),
    }

    response = session.post(f"{BASE_URL}/api/entries/", json=payload)

    is_valid = (
        is_valid_name(name)
        and 0 <= proteins <= 1000
        and 0 <= fats <= 1000
        and 0 <= carbs <= 1000
        and 0 <= calories <= 10000
    )

    assert response.status_code != 500

    if is_valid:
        assert response.status_code in (200, 201)
    else:
        assert response.status_code in (400, 422)


@settings(max_examples=100, deadline=None)
@given(entry_date=random_date_string)
def test_fuzz_invalid_date_format(session, entry_date):
    payload = {
        "name": "Тестовая запись",
        "proteins": 10,
        "fats": 5,
        "carbs": 20,
        "calories": 150,
        "entry_date": entry_date,
    }

    response = session.post(f"{BASE_URL}/api/entries/", json=payload)

    assert response.status_code != 500
    assert response.status_code in (200, 201, 422)


@settings(max_examples=100, deadline=None)
@given(
    username=st.text(min_size=0, max_size=200),
    password=st.text(min_size=0, max_size=200),
)
def test_fuzz_login_random_credentials(username, password):
    response = requests.post(f"{BASE_URL}/auth/login", data={
        "username": username,
        "password": password,
    })

    assert response.status_code != 500


@settings(max_examples=150, deadline=None)
@given(
    age=st.integers(min_value=-1000, max_value=1000),
    height=st.floats(min_value=-1000, max_value=1000, allow_nan=False),
    weight=st.floats(min_value=-1000, max_value=1000, allow_nan=False),
)
def test_fuzz_profile_invalid_ranges(session, age, height, weight):
    payload = {
        "age": age,
        "height": height,
        "weight": weight,
        "gender": "male",
        "activity": 1.55,
        "goal": "maintain",
    }

    response = session.post(f"{BASE_URL}/api/profile/", json=payload)

    assert response.status_code != 500
    assert response.status_code in (200, 422)