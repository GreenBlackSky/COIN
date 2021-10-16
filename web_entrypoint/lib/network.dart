import 'requests.dart';

Future<void> loadDataFromServerOnRegister(String name, String password) async {
  var response = await requestRegistration(name, password);
  processAuthorizationResponse(response);
  var accountsResponse = await requestAccounts();
  processAccountsResponse(accountsResponse);
  var eventsResponse = await requestCurrentMonthEvents();
  processEventsResponse(eventsResponse);
}

Future<void> loadDataFromServerOnLogin(String name, String password) async {
  var response = await requestLogin(name, password);
  processAuthorizationResponse(response);
  var accountsResponse = await requestAccounts();
  processAccountsResponse(accountsResponse);
  var eventsResponse = await requestCurrentMonthEvents();
  processEventsResponse(eventsResponse);
}

Future<void> createAccount(String name) async {
  var response = await requestCreateAccount(
    name,
  );
  var responseBody = getResponseBody(response);
  var allAccountsResponse = await requestAccounts();
  processAccountsResponse(allAccountsResponse);
  setActiveAccountAfterCreate(responseBody);
  var eventsResponse = await requestCurrentMonthEvents();
  processEventsResponse(eventsResponse);
}

Future<void> renameAccount(int id, String name) async {
  var response = await requestRenameAccount(id, name);
  var responseBody = getResponseBody(response);
  var allAccountsResponse = await requestAccounts();
  processAccountsResponse(allAccountsResponse);
  setActiveAccountAfterRename(responseBody);
  var eventsResponse = await requestCurrentMonthEvents();
  processEventsResponse(eventsResponse);
}

Future<void> deleteAccount(int id) async {
  var response = await requestDeleteAccount(id);
  var responseBody = getResponseBody(response);
  var allAccountsResponse = await requestAccounts();
  processAccountsResponse(allAccountsResponse);
  setActiveAccountAfterDelete(responseBody);
  var eventsResponse = await requestCurrentMonthEvents();
  processEventsResponse(eventsResponse);
}

Future<void> getEvents() async {
  var eventsResponse = await requestCurrentMonthEvents();
  processEventsResponse(eventsResponse);
}

Future<void> createEvent(
    DateTime dateTime, int diff, String description) async {
  var response = await requestCreateEvent(dateTime, diff, description);
  getResponseBody(response);
  response = await requestCurrentMonthEvents();
  processEventsResponse(response);
}

Future<void> editEvent(
    int id, DateTime dateTime, int diff, String description) async {
  var response = await requestEditEvent(id, dateTime, diff, description);
  getResponseBody(response);
  response = await requestCurrentMonthEvents();
  processEventsResponse(response);
}

Future<void> deleteEvent(int id) async {
  var response = await requestDeleteEvent(id);
  getResponseBody(response);
  response = await requestCurrentMonthEvents();
  processEventsResponse(response);
}
