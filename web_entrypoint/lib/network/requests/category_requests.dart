import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'session.dart';

import 'package:coin_client/common.dart';

Future<http.Response> requestCategories(int accountID) async {
  return session.post(
      'get_categories', jsonEncode(<String, dynamic>{'account_id': accountID}));
}

Future<http.Response> requestCreateCategory(
    String name, Color color, int accountID) async {
  return session.post(
      'create_category',
      jsonEncode(<String, dynamic>{
        'account_id': accountID,
        'name': name,
        'color': color.value.toRadixString(16)
      }));
}

Future<http.Response> requestEditCategory(
    int categoryID, String name, Color color, int accountID) async {
  return session.post(
      'edit_category',
      jsonEncode(<String, dynamic>{
        'account_id': accountID,
        'category_id': categoryID,
        'name': name,
        'color': color.value.toRadixString(16)
      }));
}

Future<http.Response> requestDeleteCategory(
    int categoryID, int accountID) async {
  return session.post(
      'delete_category',
      jsonEncode(<String, dynamic>{
        'account_id': accountID,
        'category_id': categoryID,
        'category_to': 0
      }));
}

Future<http.Response> requestTotalsByCategory(
    int accountID, DateTime startTime, DateTime endTime) async {
  return session.post(
      'get_totals_by_category',
      jsonEncode(<String, dynamic>{
        'account_id': accountID,
        'start_time': timestampFromDateTime(startTime),
        'end_time': timestampFromDateTime(endTime)
      }));
}
