import "dart:convert";
import 'package:http/http.dart' as http;

class Session {
  // String host = 'http://api_service:5004/';
  String host = 'http://localhost:5004/';
//TODO loose headers on error
  Map<String, String> _baseHeaders = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Access-Control-Allow-Origin': '*'
  };
  Map<String, String> _headers;

  Session() {
    this.clearSession();
  }

  void clearSession() {
    this._headers = new Map<String, String>.from(_baseHeaders);
  }

  Future<http.Response> post(String url, [dynamic data]) async {
    if (data == null) {
      data = jsonEncode(<String, String>{});
    }
    http.Response response =
        await http.post(host + url, body: data, headers: this._headers);
    var responseData = jsonDecode(response.body);
    String jwt = responseData['access_token'];
    if (response.statusCode == 200 && jwt != null) {
      this._headers['Authorization'] = "Bearer " + jwt;
    }
    return response;
  }
}

var session = Session();
