import 'dart:convert';
import 'package:http/http.dart' as http;

import 'session.dart';

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
