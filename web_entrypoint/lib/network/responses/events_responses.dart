import 'package:http/http.dart' as http;

import 'utils.dart';
import 'package:coin_client/storage.dart';

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
