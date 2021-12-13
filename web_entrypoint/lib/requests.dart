import 'dart:convert';
import 'package:coin_client/storage.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'session.dart';
import 'common.dart';

Future<http.Response> requestRegistration(String name, String password) async {
  return session.post(
      'register',
      jsonEncode(<String, String>{
        'name': name,
        'password': password,
      }));
}

Future<http.Response> requestLogin(String name, String password) async {
  return session.post(
      'login',
      jsonEncode(<String, String>{
        'name': name,
        'password': password,
      }));
}

Future<http.Response> requestEditUser(
    String name, String password, String newPassword) async {
  return session.post(
      'edit_user',
      jsonEncode(<String, dynamic>{
        'name': name,
        'old_pass': password,
        'new_pass': newPassword
      }));
}

Future<http.Response> requestAccounts() async {
  return session.post('get_accounts');
}

Future<http.Response> requestCreateAccount(String accountName) async {
  return session.post(
      'create_account',
      jsonEncode(<String, String>{
        'name': accountName,
      }));
}

Future<http.Response> requestRenameAccount(
    int accountID, String accountName) async {
  return session.post(
      'edit_account',
      jsonEncode(
          <String, dynamic>{'name': accountName, 'account_id': accountID}));
}

Future<http.Response> requestDeleteAccount(int accountID) async {
  return session.post(
      'delete_account',
      jsonEncode(<String, int>{
        'account_id': accountID,
      }));
}

Future<http.Response> requestCategories() async {
  return session.post('get_categories',
      jsonEncode(<String, dynamic>{'account_id': storage.account}));
}

Future<http.Response> requestCreateCategory(
    String name, String description, Color color) async {
  return session.post(
      'create_category',
      jsonEncode(<String, dynamic>{
        'account_id': storage.account,
        'name': name,
        'description': description,
        'color': color.toString()
      }));
}

Future<http.Response> requestEditCategory(
    int categoryID, String name, String description, Color color) async {
  return session.post(
      'edit_category',
      jsonEncode(<String, dynamic>{
        'account_id': storage.account,
        'category_id': categoryID,
        'name': name,
        'description': description,
        'color': color.toString()
      }));
}

Future<http.Response> requestDeleteCategory(int categoryID) async {
  return session.post(
      'delete_categorys',
      jsonEncode(<String, dynamic>{
        'account_id': storage.account,
        'category_id': categoryID
      }));
}

Future<http.Response> requestBalance(int accountID, DateTime dateTime) async {
  return session.post(
      'get_balance',
      jsonEncode(<String, dynamic>{
        'account_id': accountID,
        'category_id': storage.category,
        'timestamp': timestampFromDateTime(dateTime),
      }));
}

Future<http.Response> requestEvents(
    int accountID, DateTime startTime, DateTime endTime,
    {int label = -1}) async {
  var body = <String, int>{
    'account_id': accountID,
    'start_time': timestampFromDateTime(startTime),
    'end_time': timestampFromDateTime(endTime),
    'category_id': storage.category
  };
  if (label != -1) {
    body['label'] = label;
  }
  return session.post('get_events', jsonEncode(body));
}

Future<http.Response> requestCreateEvent(
    int accountID, DateTime eventTime, int diff, String description,
    {int label = -1}) async {
  var body = <String, dynamic>{
    'account_id': accountID,
    'category_id': storage.category,
    'event_time': timestampFromDateTime(eventTime),
    'diff': diff,
    'description': description
  };
  if (label != -1) {
    body['label'] = label;
  }
  return session.post('create_event', jsonEncode(body));
}

Future<http.Response> requestEditEvent(
    int eventID, DateTime eventTime, int diff, String description,
    {int label = -1}) async {
  var body = <String, dynamic>{
    'event_id': eventID,
    'category_id': storage.category,
    'event_time': timestampFromDateTime(eventTime),
    'diff': diff,
    'description': description
  };
  if (label != -1) {
    body['label'] = label;
  }
  return session.post('edit_event', jsonEncode(body));
}

Future<http.Response> requestDeleteEvent(int eventID) async {
  return session.post(
      'delete_event',
      jsonEncode(<String, dynamic>{
        'event_id': eventID,
      }));
}
