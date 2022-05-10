"""Events stuff tests."""

import pytest

from .utils import async_session, base_test, TestCase
from .conftest import (
    full_user_data,
    base_category_data,
    account_data,
    one_user_db,
    simple_user,
    base_event,
)

from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


def create_event_request():
    request = base_event()
    del request["id"]
    return request


def create_event_response():
    return ({"status": "OK", "event": base_event()}, 200)


def one_event_db():
    return {
        "users": [full_user_data()],
        "accounts": [account_data()],
        "categories": [base_category_data()],
        "events": [base_event()],
    }


# create_event
# balance_changes_on_create
# events_at_months_start
# add_event_at_previous_month
# create_event_with_duplicate_description
# create_event_with_too_long_description
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # create event
            one_user_db(),
            simple_user(),
            create_event_request(),
            create_event_response(),
            one_event_db(),
        )
    ],
    ids=["create event"],
)
async def test_create_event(case: TestCase):
    await base_test("/create_event", case)


def get_all_events_request():
    return {
        "account_id": 1,
        "start_time": None,
        "end_time": None,
    }


def get_all_events_response():
    return (
        {
            "status": "OK",
            "events": [base_event()],
        },
        200,
    )


# filter_events_after
# filter_events_before
# events_with_year_between
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # get all events
            one_event_db(),
            simple_user(),
            get_all_events_request(),
            get_all_events_response(),
            one_event_db(),
        )
    ],
    ids=["get all events"],
)
async def test_get_events(case: TestCase):
    await base_test("/get_events", case)


def edited_event_data():
    event = base_event()
    return {
        "user_id": event["user_id"],
        "account_id": event["account_id"],
        "id": event["id"],
        "category_id": event["category_id"],
        "event_time": event["event_time"],
        "diff": 10,
        "description": "Edited",
    }


def edit_event_request():
    request = edited_event_data()
    del request["user_id"]
    request["event_id"] = request.pop("id")
    return request


def edit_event_response():
    return ({"status": "OK", "event": edited_event_data()}, 200)


def edited_event_data_db():
    return {
        "users": [full_user_data()],
        "accounts": [account_data()],
        "categories": [base_category_data()],
        "events": [edited_event_data()],
    }


# edit event data
# move event slightly
# move event into far future
# move event into distant past
# edit non_existent_event
# edit event_with_duplicate_description
# edit event_with_too_long_description
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # edit event data
            one_event_db(),
            simple_user(),
            edit_event_request(),
            edit_event_response(),
            edited_event_data_db(),
        )
    ],
    ids=["edit event data"],
)
async def test_edit_event(case: TestCase):
    await base_test("/edit_event", case)


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
