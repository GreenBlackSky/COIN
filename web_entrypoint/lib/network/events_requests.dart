import 'dart:convert';
import 'package:http/http.dart' as http;

import 'session.dart';
import 'package:coin_client/views/widgets/common/common.dart';

Future<http.Response> requestEvents(
    int accountID, DateTime startTime, DateTime endTime) async {
  var body = <String, int>{
    'account_id': accountID,
    'start_time': timestampFromDateTime(startTime),
    'end_time': timestampFromDateTime(endTime),
  };
  return session.post('get_events', jsonEncode(body));
}

Future<http.Response> requestCreateEvent(int accountID, DateTime eventTime,
    int diff, String description, int categoryID) async {
  var body = <String, dynamic>{
    'account_id': accountID,
    'category_id': categoryID,
    'event_time': timestampFromDateTime(eventTime),
    'diff': diff,
    'description': description
  };
  return session.post('create_event', jsonEncode(body));
}

Future<http.Response> requestEditEvent(int eventID, int accountID,
    DateTime eventTime, int diff, String description, int categoryID) async {
  var body = <String, dynamic>{
    'event_id': eventID,
    'account_id': accountID,
    'category_id': categoryID,
    'event_time': timestampFromDateTime(eventTime),
    'diff': diff,
    'description': description
  };
  return session.post('edit_event', jsonEncode(body));
}

Future<http.Response> requestDeleteEvent(int eventID, int accountID) async {
  return session.post(
      'delete_event',
      jsonEncode(
          <String, dynamic>{'event_id': eventID, 'account_id': accountID}));
}
