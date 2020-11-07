import api
from datetime import datetime


if __name__ == "__main__":
    today = datetime.date(datetime(year=1000, month=1, day=1))

    user_uid = api.add_user(today, 10)

    balance = api.get_balance(user_uid, today.replace(day=2))
    assert balance['balance'] == 10

    api.add_event(user_uid, today.replace(day=4), 5, api.Category.Income, "")
    balance = api.get_balance(user_uid, today.replace(day=4))
    assert balance['balance'] == 15

    api.correct(user_uid, today.replace(day=6), 5, "")
    balance = api.get_balance(user_uid, today.replace(day=6))
    assert balance['balance'] == 5

    print(api.get_month_data(user_uid, today))
