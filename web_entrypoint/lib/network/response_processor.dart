import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'package:coin_client/storage.dart';

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
  if (storage.accounts.length >= storage.accountIndex) {
    storage.accountIndex = storage.accounts.length - 1;
  }
}

void processCategories(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.categories.clear();
  for (Map<String, dynamic> categoryJson in responseBody['categories']) {
    categoryJson['color'] = Color(int.parse(categoryJson['color'], radix: 16));
    storage.categories.add(categoryJson);
  }
}

void processEditCategoryResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  var newVal = responseBody['category'];
  newVal['color'] = Color(int.parse(newVal['color'], radix: 16));

  var oldVal = storage.categories.where((element) {
    return element['id'] == responseBody['category']['id'];
  }).first;
  int index = storage.categories.indexOf(oldVal);
  storage.categories[index] = newVal;
}

void processRemoveCategoryResponse(http.Response response) {}

void processMonthStartBalanceResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.monthStartBalance = responseBody['balance'];
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
