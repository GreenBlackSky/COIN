import 'dart:convert';
import 'package:http/http.dart' as http;

import 'session.dart';
import 'package:coin_client/views/widgets/common/common.dart';

Future<http.Response> requestBalance(int accountID, DateTime dateTime) async {
  return session.post(
      'get_balance',
      jsonEncode(<String, dynamic>{
        'account_id': accountID,
        'timestamp': timestampFromDateTime(dateTime),
      }));
}
