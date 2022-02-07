import 'package:http/http.dart' as http;

import 'utils.dart';
import 'package:coin_client/storage.dart';

void processAuthorizationResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.name = responseBody['user']['name'];
}

void processMonthStartBalanceResponse(http.Response response) {
  var responseBody = getResponseBody(response);
  storage.monthStartBalance = responseBody['balance'];
}
