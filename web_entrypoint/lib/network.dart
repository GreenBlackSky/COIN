import 'requests.dart';
import 'responseprocessor.dart';

import 'storage.dart';

Future<void> loadDataFromServerOnRegister(String name, String password) async {
  await requestRegistration(name, password).then(processAuthorizationResponse);
  await requestAccounts().then(processAccountsResponse);
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
}

Future<void> loadDataFromServerOnLogin(String name, String password) async {
  await requestLogin(name, password).then(processAuthorizationResponse);
  await requestAccounts().then(processAccountsResponse);
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
}

Future<void> editUser(String name, String password, String newPassword) async {
  await requestEditUser(name, password, newPassword);
}

Future<void> createAccount(String name) async {
  var response = await requestCreateAccount(
    name,
  );
  var responseBody = getResponseBody(response);
  await requestAccounts().then(processAccountsResponse);
  setActiveAccountAfterCreate(responseBody);
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
}

Future<void> renameAccount(int id, String name) async {
  var response = await requestRenameAccount(id, name);
  var responseBody = getResponseBody(response);
  await requestAccounts().then(processAccountsResponse);
  setActiveAccountAfterRename(responseBody);
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
}

Future<void> deleteAccount(int id) async {
  var response = await requestDeleteAccount(id);
  var responseBody = getResponseBody(response);
  await requestAccounts().then(processAccountsResponse);
  setActiveAccountAfterDelete(responseBody);
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
}

Future<void> getEvents() async {
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
}

Future<void> createEvent(
    DateTime dateTime, int diff, String description) async {
  var response =
      await requestCreateEvent(storage.account, dateTime, diff, description);
  getResponseBody(response);
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
}

Future<void> editEvent(
    int id, DateTime dateTime, int diff, String description) async {
  var response = await requestEditEvent(id, dateTime, diff, description);
  getResponseBody(response);
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
}

Future<void> deleteEvent(int id) async {
  var response = await requestDeleteEvent(id);
  getResponseBody(response);
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
}
