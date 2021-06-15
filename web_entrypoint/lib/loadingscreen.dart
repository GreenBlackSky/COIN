import 'dart:convert';

import 'package:coin_client/loadinganimation.dart';
import 'package:http/http.dart' as http;

import 'package:flutter/animation.dart';
import 'package:flutter/material.dart';

import 'common.dart';
import 'session.dart';
import 'storage.dart';

class LoadingScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final UserArgs args = ModalRoute.of(context).settings.arguments as UserArgs;

    return Scaffold(body: buildForm(Loader(args: args)));
  }
}

class Loader extends StatefulWidget {
  final UserArgs args;
  Loader({Key key, @required this.args}) : super(key: key);

  @override
  _LoaderState createState() => _LoaderState();
}

class _LoaderState extends State<Loader> with SingleTickerProviderStateMixin {
  Animation<double> animation;
  AnimationController controller;

  @override
  void initState() {
    super.initState();
    this.loadDataFromServer();
    controller =
        AnimationController(duration: const Duration(seconds: 1), vsync: this);
    animation = Tween<double>(begin: 10, end: 100).animate(controller);
    controller.forward();
    controller.repeat(reverse: true);
  }

  @override
  Widget build(BuildContext context) => LoadingAnimation(animation: animation);

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  // TODO move requests into separate class
  Future<void> loadDataFromServer() async {
    try {
      http.Response authRespose = await this.requestAuthorization();
      this.processAuthorizationResponse(authRespose);
      http.Response accountsResponse = await this.requestAccounts();
      this.processAccountsResponse(accountsResponse);
      // http.Response eventsResponse = await this.requestEvents();
      // this.processEventsResponse(eventsResponse);
    } catch (e) {
      displayError(this.context, e.toString());
      session.clearSession();
      if (widget.args.regestration) {
        Navigator.of(this.context).pushReplacementNamed("/signup");
      } else {
        Navigator.of(this.context).pushReplacementNamed("/login");
      }
      return;
    }
    Navigator.of(this.context).pushReplacementNamed("/main");
  }

  Future<http.Response> requestAuthorization() async {
    String method = widget.args.regestration ? 'register' : 'login';
    return await session.post(
        method,
        jsonEncode(<String, String>{
          'name': widget.args.name,
          'password': widget.args.password,
        }));
  }

  void processAuthorizationResponse(http.Response response) {
    if (response.statusCode != 200) {
      throw Exception("Problem with connection.");
    }
    Map<String, dynamic> responseBody = jsonDecode(response.body);
    if (responseBody['status'] != 'OK') {
      throw Exception(responseBody['status']);
    }
    storage.name = responseBody['user']['name'];
  }

  Future<http.Response> requestAccounts() async {
    return await session.post('get_accounts');
  }

  void processAccountsResponse(http.Response response) {
    Map<String, dynamic> responseBody = jsonDecode(response.body);
    if (responseBody['status'] != 'OK') {
      throw Exception(responseBody['status']);
    }
    storage.account = responseBody['accounts'][0]['id'];
    for (Map<String, dynamic> accountJson in responseBody['accounts']) {
      storage.accounts[accountJson['id']] = accountJson['name'];
    }
  }

  Future<http.Response> requestEvents() async {
    return await session.post('get_events');
  }

  void processEventsResponse(http.Response response) {
    storage.events = [];
  }
}
