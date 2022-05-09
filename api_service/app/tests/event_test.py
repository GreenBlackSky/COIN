"""Events stuff tests."""

import pytest
from pytest_lazyfixture import lazy_fixture

from .utils import async_session, base_test
from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


@pytest.fixture
def create_event_request(base_event):
    request = dict(base_event)
    del request["id"]
    return request


@pytest.fixture
def create_event_response(base_event):
    return {"status": "OK", "event": base_event}


@pytest.fixture
def one_event_db(full_user_data, account_data, base_category_data, base_event):
    return {
        "users": [full_user_data],
        "accounts": [account_data],
        "categories": [base_category_data],
        "events": [base_event],
    }


# create_event
# balance_changes_on_create
# events_at_months_start
# add_event_at_previous_month
# create_event_with_duplicate_description
# create_event_with_too_long_description
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # create event
            lazy_fixture("one_user_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("create_event_request"),
            200,
            lazy_fixture("create_event_response"),
            lazy_fixture("one_event_db"),
        ]
    ],
    ids=["create event"],
)
async def test_create_event(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/create_event",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )


@pytest.fixture
def get_all_events_request():
    return {
        "account_id": 1,
        "start_time": None,
        "end_time": None,
    }


@pytest.fixture
def get_all_events_response(base_event):
    return {
        "status": "OK",
        "events": [base_event],
    }


# filter_events_after
# filter_events_before
# events_with_year_between
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # get all events
            lazy_fixture("one_event_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("get_all_events_request"),
            200,
            lazy_fixture("get_all_events_response"),
            lazy_fixture("one_event_db"),
        ]
    ],
    ids=["get all events"],
)
async def test_get_events(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/get_events",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )


@pytest.fixture
def edited_event_data(base_event):
    return {
        "user_id": base_event["user_id"],
        "account_id": base_event["account_id"],
        "id": base_event["id"],
        "category_id": base_event["category_id"],
        "event_time": base_event["event_time"],
        "diff": 10,
        "description": "Edited",
    }


@pytest.fixture
def edit_event_request(edited_event_data):
    request = dict(edited_event_data)
    del request["user_id"]
    request["event_id"] = request.pop("id")
    return request


@pytest.fixture
def edit_event_response(edited_event_data):
    return {"status": "OK", "event": edited_event_data}


@pytest.fixture
def edited_event_data_db(
    full_user_data, account_data, base_category_data, edited_event_data
):
    return {
        "users": [full_user_data],
        "accounts": [account_data],
        "categories": [base_category_data],
        "events": [edited_event_data],
    }


# edit event data
# move event slightly
# move event into far future
# move event into distant past
# edit non_existent_event
# edit event_with_duplicate_description
# edit event_with_too_long_description
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # edit event data
            lazy_fixture("one_event_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("edit_event_request"),
            200,
            lazy_fixture("edit_event_response"),
            lazy_fixture("edited_event_data_db"),
        ]
    ],
    ids=["edit event data"],
)
async def test_edit_event(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/edit_event",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )


# delete_event
# delete_non_existant_event
def test_delete_event():
    pass


# get_balance
# balance_changes_on_edit_event
# balance_changes_on_delete_event
# balance_with_no_events
# balance_after_events
# balance_between_events
# balance_before_events
# events_in_two_months
def test_get_balance():
    pass


# get_balance
# balance_changes_on_edit_event
# balance_changes_on_delete_event
# balance_with_no_events
# balance_after_events
# balance_between_events
# balance_before_events
# events_in_two_months
def test_get_totals_by_category():
    pass
