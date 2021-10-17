import 'dart:convert';
import 'package:http/http.dart' as http;

import 'storage.dart';

Map<String, dynamic> getResponseBody(http.Response response) {
  if (response.statusCode != 200 &&
      response.statusCode != 401 &&
      response.statusCode != 412) {
    throw Exception("Problem with connection.");
  }
  Map<String, dynamic> responseBody = jsonDecode(response.body);
  if (responseBody['status'] != 'OK') {
    throw Exception(responseBody['status']);
  }
  return responseBody;
}

void processAuthorizationResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.name = responseBody['user']['name'];
}

void processAccountsResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.account = responseBody['accounts'][0]['id'];
  storage.accounts.clear();
  for (Map<String, dynamic> accountJson in responseBody['accounts']) {
    storage.accounts[accountJson['id']] = accountJson['name'];
  }
}

void setActiveAccountAfterCreate(Map<String, dynamic> responseBody) {
  int accountID = responseBody['account']['id'];
  String accountName = responseBody['account']['name'];
  storage.accounts[accountID] = accountName;
  storage.account = accountID;
}

void setActiveAccountAfterRename(Map<String, dynamic> responseBody) {
  int accountID = responseBody['account']['id'];
  storage.account = accountID;
}

void setActiveAccountAfterDelete(Map<String, dynamic> responseBody) {
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
}

void processEventsResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.events.clear();
  for (Map<String, dynamic> eventJson in responseBody['events']) {
    storage.events.add(eventJson);
  }
  storage.events.sort((event1, event2) {
    return event1['event_time'] - event2['event_time'];
  });
}
