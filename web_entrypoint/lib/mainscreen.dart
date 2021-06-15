import 'dart:convert';
import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'common.dart';
import 'session.dart';
import 'storage.dart';

class MainScreen extends StatelessWidget {
  final MainWidget _mainWdget = new MainWidget();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          leading: new Container(),
          title: TextButton(
            style: TextButton.styleFrom(
              padding: const EdgeInsets.all(16.0),
              primary: Colors.white,
              textStyle: const TextStyle(fontSize: 20),
            ),
            onPressed: _mainWdget.openAccountsPanel,
            child: Text(storage.accounts[storage.account]),
          ),
          actions: <Widget>[buildPopUpMenu(context)]),
      body: Center(
        child: _mainWdget,
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          //TODO Add event
        },
        child: Icon(Icons.add),
      ),
    );
  }

  Widget buildPopUpMenu(BuildContext context) {
    return PopupMenuButton<String>(
      onSelected: (String value) {
        switch (value) {
          case 'Logout':
            session.post('logout').catchError((_) {});
            session.clearSession();
            Navigator.of(context).pushNamed('/login');
            break;
          case 'Settings':
            Navigator.of(context).pushNamed('/settings');
            break;
        }
      },
      itemBuilder: (BuildContext context) {
        return [
          PopupMenuItem<String>(value: "Settings", child: Text("Settings")),
          PopupMenuItem<String>(value: "Logout", child: Text("Logout"))
        ];
      },
    );
  }
}

class MainWidget extends StatefulWidget {
  @override
  _MainState createState() => _MainState();
  void openAccountsPanel() {
    log("A PANEL");
  }
}

class _MainState extends State<MainWidget> {
  void _sendRequest() {
    session.post('test_login').then(_processResponse).catchError((err) {
      displayError(context, "Connection error ${err.toString()}");
    });
  }

  void _processResponse(http.Response response) {
    if (response.statusCode != 200) {
      displayError(context, "Problem with connection.");
    } else {
      Map<String, dynamic> responseBody = jsonDecode(response.body);
      displayError(context, responseBody['status']);
    }
  }

  @override
  Widget build(BuildContext context) {
    // TODO build events
    return Form(
        child: Column(mainAxisSize: MainAxisSize.min, children: <Widget>[
      Text(
        "No events yet",
        style: Theme.of(context).textTheme.headline2,
      ),
      buildButton("Try", _sendRequest),
    ]));
  }
}
