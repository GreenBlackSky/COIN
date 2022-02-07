import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'utils.dart';
import 'package:coin_client/storage.dart';

void processCategories(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.categories.clear();
  for (Map<String, dynamic> categoryJson in responseBody['categories']) {
    categoryJson['color'] = Color(int.parse(categoryJson['color'], radix: 16));
    storage.categories.add(categoryJson);
  }
}

void processAddCategoryResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  var categoryJson = responseBody['category'];
  categoryJson['color'] = Color(int.parse(categoryJson['color'], radix: 16));
  storage.categories.add(categoryJson);
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

void processRemoveCategoryResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  var category = storage.categories.where((element) {
    return element['id'] == responseBody['category']['id'];
  }).first;
  storage.categories.remove(category);
}

void processTotalsByCategory(http.Response response) {
  var responseBody = getResponseBody(response);
  for (String key in responseBody['totals'].keys) {
    storage.totals[int.parse(key)] = responseBody['totals'][key];
  }
}
