"""Accounts stuff tests."""

from datetime import datetime

from tests.test_base import BaseTest


class EventTest(BaseTest):
    """Accounts stuff tests."""

    def _create_event(self, session, account, confirmed=False):
        event_data = {
            'account_id': account['id'],
            'event_time': datetime.now().timestamp(),
            'diff': 10,
            'description': "TEST",
            'confirmed': confirmed
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

    def _delete_event(self, session, event_id):
        response = session.post(
            url=self.HOST+"delete_event",
            json={'event_id': event_id}
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
        deleted_event = self._delete_event(session, event['id'])
        self.assertDictEqual(event, deleted_event, "Problems with event data")
        none_event = self._get_first_event(session, account['id'])
        self.assertEqual(none_event, {}, "None none event")

    def test_confirm_event(self):
        """Test confirming events."""
        session, _ = self.prepare()
        response = session.post(url=self.HOST+"get_accounts")
        (account,) = response.json()['accounts']
        created_event = self._create_event(session, account)

        response = session.post(
            url=self.HOST+"confirm_event",
            json={'event_id': created_event['id'], 'confirm': True}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertEqual(response.json()['status'], 'OK', "Wrong status code")

        confirmed_event = self._get_first_event(session, account['id'])
        self.assertTrue(confirmed_event['confirmed'])

    def test_unconfirm_event(self):
        """Test confirming events."""
        session, _ = self.prepare()
        response = session.post(url=self.HOST+"get_accounts")
        (account,) = response.json()['accounts']
        created_event = self._create_event(session, account, True)

        response = session.post(
            url=self.HOST+"confirm_event",
            json={'event_id': created_event['id'], 'confirm': False}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertEqual(response.json()['status'], 'OK', "Wrong status code")

        confirmed_event = self._get_first_event(session, account['id'])
        self.assertFalse(confirmed_event['confirmed'])

    def test_edit_event(self):
        """Test editing fields of event."""
        session, _ = self.prepare()
        response = session.post(url=self.HOST+"get_accounts")
        (account,) = response.json()['accounts']
        created_event = self._create_event(session, account, True)

        edited_time = datetime.now().timestamp() + 100
        response = session.post(
            url=self.HOST+"edit_event",
            json={
                'event_id': created_event['id'],
                'event_time': edited_time,
                'diff': 20,
                'description': "EDITED"
            }
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertEqual(response.json()['status'], 'OK', "Wrong status code")

        edited_event = self._get_first_event(session, account['id'])
        self.assertEqual(edited_event['event_time'], edited_time, "Wrong time")
        self.assertEqual(edited_event['diff'], 20, "Wrong diff")
        self.assertEqual(
            edited_event['description'],
            'EDITED',
            "Wrong description"
        )

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

    # def test_edit_non_existent_event():
    #     pass

    # def test_confiem_non_existent_event():
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
