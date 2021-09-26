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

void processAccountsResponse(http.Response response) {
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
