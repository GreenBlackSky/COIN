import 'dart:convert';
import 'package:http/http.dart' as http;

import 'session.dart';
import 'storage.dart';

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
  if (response.statusCode != 200) {
    throw Exception("Problem with connection.");
  }
  Map<String, dynamic> responseBody = jsonDecode(response.body);
  if (responseBody['status'] != 'OK') {
    throw Exception(responseBody['status']);
  }
  storage.name = responseBody['user']['name'];
}

Future<http.Response> requestAccounts() async {
  return await session.post('get_accounts');
}

Future<http.Response> requestCreateAccount(accountName) async {
  return await session.post(
      'create_account',
      jsonEncode(<String, String>{
        'name': accountName,
      }));
}

void processCreatingAccountResponse(http.Response response) {
  if (response.statusCode != 200) {
    throw Exception("Problem with connection.");
  }
  Map<String, dynamic> responseBody = jsonDecode(response.body);
  if (responseBody['status'] != 'OK') {
    throw Exception(responseBody['status']);
  }
  int accountID = responseBody['account']['id'];
  String accountName = responseBody['account']['name'];
  storage.accounts[accountID] = accountName;
  storage.account = accountID;
}

Future<http.Response> requestDeleteAccount(int accountID) async {
  return await session.post(
      'delete_account',
      jsonEncode(<String, int>{
        'account_id': accountID,
      }));
}

void processDeletingAccountResponse(http.Response response) {
  if (response.statusCode != 200) {
    throw Exception("Problem with connection.");
  }
  Map<String, dynamic> responseBody = jsonDecode(response.body);
  if (responseBody['status'] != 'OK') {
    throw Exception(responseBody['status']);
  }
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

void processAccountsResponse(http.Response response) {
  if (response.statusCode != 200) {
    throw Exception("Problem with connection.");
  }
  Map<String, dynamic> responseBody = jsonDecode(response.body);
  if (responseBody['status'] != 'OK') {
    throw Exception(responseBody['status']);
  }
  storage.account = responseBody['accounts'][0]['id'];
  for (Map<String, dynamic> accountJson in responseBody['accounts']) {
    storage.accounts[accountJson['id']] = accountJson['name'];
  }
}

Future<http.Response> requestEvents() async {
  return await session.post('get_events');
}

void processEventsResponse(http.Response response) {
  storage.events = [];
}
