import 'package:http/http.dart' as http;

import 'utils.dart';

import 'package:coin_client/storage.dart';

void processAccountsResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  if (storage.accountIndex == -1) {
    storage.accountIndex = 0;
  }
  storage.accounts.clear();
  for (Map<String, dynamic> accountJson in responseBody['accounts']) {
    storage.accounts.add(accountJson);
  }
}

void setActiveAccountAfterCreate(Map<String, dynamic> responseBody) {
  storage.accountIndex = storage.accounts.length - 1;
}

void setActiveAccountAfterDelete(Map<String, dynamic> responseBody) {
  if (storage.accounts.length <= storage.accountIndex) {
    storage.accountIndex = storage.accounts.length - 1;
  }
}
