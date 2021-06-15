"""Accounts stuff tests."""

from datetime import datetime

from tests.test_base import BaseTest


class EventTest(BaseTest):
    """Accounts stuff tests."""

    def _create_event(self, session, account):
        event_data = {
            'account_id': account['id'],
            'event_time': datetime.now().timestamp(),
            'diff': 10,
            'description': "TEST",
            'confirmed': True
        }
        response = session.post(
            url=self.HOST+"create_event",
            json=event_data
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': "OK"},
            response.json(),
            "Wrong answear"
        )
        event = response.json().get('event')
        self.assertIsNotNone(event, "No event")
        self.assertDictContainsSubset(
            event_data, event, 'Incorrect data in event'
        )
        return event

    def _get_first_event(self, session, account_id):
        response = session.post(
            url=self.HOST+"get_first_event",
            json={'account_id': account_id}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertEqual(response.json()['status'], 'OK', "Wrong status code")
        self.assertIn('event', response.json(), "No event in response")
        return response.json()['event']

    def test_create_event_unauthorized(self):
        """Try create event without authorization."""
        session, _ = self.prepare()
        response = session.post(url=self.HOST+"get_accounts")
        (account,) = response.json()['accounts']
        self.logout(session)
        response = session.post(
            url=self.HOST+"create_event",
            json={
                'account_id': account['id'],
                'event_time': datetime.now().timestamp(),
                'diff': 10,
                'description': "TEST",
                'confirmed': True
            }
        )
        self.assertEqual(response.status_code, 401, "Wrong response code")
        self.assertDictContainsSubset(
            {"status": "unauthorized access"},
            response.json(),
            "Wrong answear"
        )

    # def test_delete_event_unauthorized():
    #     pass

    # def test_confirm_event_unauthorized():
    #     pass

    # def test_edit_event_unauthorized():
    #     pass

    # def test_get_events_unauthorized():
    #     pass

    # def test_get_first_event_unauthorized():
    #     pass

    def test_create_event(self):
        """Test creating new event."""
        session, _ = self.prepare()
        response = session.post(url=self.HOST+"get_accounts")
        (account,) = response.json()['accounts']
        created_event = self._create_event(session, account)
        event = self._get_first_event(session, account['id'])
        self.assertDictEqual(event, created_event, "Problems with event data")

    def test_delete_event(self):
        """Test creating new event."""
        session, _ = self.prepare()
        response = session.post(url=self.HOST+"get_accounts")
        (account,) = response.json()['accounts']
        created_event = self._create_event(session, account)
        event = self._get_first_event(session, account['id'])
        self.assertDictEqual(event, created_event, "Problems with event data")
        response = session.post(
            url=self.HOST+"delete_event",
            json={'event_id': event['id']}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertEqual(response.json()['status'], 'OK', "Wrong status code")
        self.assertIn('event', response.json(), "No event in response")
        self.assertDictEqual(
            event,
            response.json()['event'],
            "Problems with event data"
        )
        none_event = self._get_first_event(session, account['id'])
        self.assertEqual(none_event, {}, "None none event")

    # def test_confirm_event():
    #     pass

    # def test_edit_event():
    #     pass

    # def test_total_changes_on_create(self):
    #     pass

    # def test_total_changes_on_edit(self):
    #     pass

    # def test_total_changes_on_delete(self):
    #     pass

    # def test_get_events():
    #     pass

    # def test_get_first_event():
    #     pass

    # def test_filter_events_after():
    #     pass

    # def test_filter_events_before():
    #     pass

    # def test_delete_non_existant_event():
    #     pass

    # def test_confirm_non_existent_event():
    #     pass

    # def test_edit_non_event():
    #     pass

    # def test_create_event_with_duplicate_description():
    #     pass

    # def test_edit_event_with_duplicate_description():
    #     pass

    # def test_create_event_with_too_long_description():
    #     pass

    # def test_edit_event_with_too_long_description():
    #     pass

    # def test_create_event_on_wrong_acc(self):
    #     pass

    # def test_edit_event_on_wrong_acc(self):
    #     pass

    # def test_delete_event_on_wrong_acc(self):
    #     pass
