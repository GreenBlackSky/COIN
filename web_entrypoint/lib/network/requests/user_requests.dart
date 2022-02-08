import 'dart:convert';
import 'package:http/http.dart' as http;

import 'session.dart';

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
