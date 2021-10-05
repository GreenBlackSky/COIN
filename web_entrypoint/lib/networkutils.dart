import 'dart:convert';
import 'package:http/http.dart' as http;

import 'session.dart';
import 'storage.dart';

Map<String, dynamic> getResponseBody(http.Response response) {
  if (response.statusCode != 200) {
    throw Exception("Problem with connection.");
  }
  Map<String, dynamic> responseBody = jsonDecode(response.body);
  if (responseBody['status'] != 'OK') {
    throw Exception(responseBody['status']);
  }
  return responseBody;
}

Future<http.Response> requestRegistration(String name, String password) async {
  return await session.post(
      'register',
      jsonEncode(<String, String>{
        'name': name,
        'password': password,
      }));
}

Future<http.Response> requestLogin(String name, String password) async {
  return await session.post(
      'login',
      jsonEncode(<String, String>{
        'name': name,
        'password': password,
      }));
}

void processAuthorizationResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.name = responseBody['user']['name'];
}

Future<http.Response> requestAccounts() async {
  return await session.post('get_accounts');
}

void processAccountsResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.account = responseBody['accounts'][0]['id'];
  for (Map<String, dynamic> accountJson in responseBody['accounts']) {
    storage.accounts[accountJson['id']] = accountJson['name'];
  }
}

Future<http.Response> requestCreateAccount(String accountName) async {
  return await session.post(
      'create_account',
      jsonEncode(<String, String>{
        'name': accountName,
      }));
}

void processCreatingAccountResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  int accountID = responseBody['account']['id'];
  String accountName = responseBody['account']['name'];
  storage.accounts[accountID] = accountName;
  storage.account = accountID;
}

Future<http.Response> requestRenameAccount(
    int accountID, String accountName) async {
  return await session.post(
      'edit_account',
      jsonEncode(
          <String, dynamic>{'name': accountName, 'account_id': accountID}));
}

void processReneamingAccountResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  int accountID = responseBody['account']['id'];
  String accountName = responseBody['account']['name'];
  storage.accounts[accountID] = accountName;
}

Future<http.Response> requestDeleteAccount(int accountID) async {
  return await session.post(
      'delete_account',
      jsonEncode(<String, int>{
        'account_id': accountID,
      }));
}

void processDeletingAccountResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  int accountID = responseBody['account']['id'];
  if (storage.account == accountID) {
    var accounts = List.from(storage.accounts.keys);
    var index = accounts.indexOf(accountID);
    if (index == 0) {
      storage.account = accounts[index + 1];
    } else {
      storage.account = accounts[index - 1];
    }
  }
  storage.accounts.remove(accountID);
}

Future<http.Response> requestEvents(int start_time, int end_time,
    {int label = -1}) async {
  var body = <String, int>{
    'account_id': storage.account,
    'start_time': start_time,
    'end_time': end_time
  };
  if (label != -1) {
    body['label'] = label;
  }
  return await session.post('get_events', jsonEncode(body));
}

void processEventsResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  for (Map<String, dynamic> eventJson in responseBody['events']) {
    storage.events.add(eventJson);
  }
}
