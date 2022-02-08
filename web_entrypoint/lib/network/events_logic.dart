import 'requests/events_requests.dart';
import 'responses/utils.dart';
import 'common.dart';

import 'package:coin_client/storage.dart';

Future<void> createEvent(
    DateTime dateTime, int diff, String description, int categoryID) async {
  var response = await requestCreateEvent(
      storage.accounts[storage.accountIndex]['id'],
      dateTime,
      diff,
      description,
      categoryID);
  getResponseBody(response);
  await syncData();
}

Future<void> editEvent(int id, DateTime dateTime, int diff, String description,
    int categoryID) async {
  var response = await requestEditEvent(
      id,
      storage.accounts[storage.accountIndex]['id'],
      dateTime,
      diff,
      description,
      categoryID);
  getResponseBody(response);
  await syncData();
}

Future<void> deleteEvent(int id) async {
  var response = await requestDeleteEvent(
      id, storage.accounts[storage.accountIndex]['id']);
  getResponseBody(response);
  await syncData();
}
