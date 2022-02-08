import 'dart:convert';
import 'package:http/http.dart' as http;

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
