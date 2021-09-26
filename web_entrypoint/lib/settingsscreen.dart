import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'common.dart';
import 'session.dart';
import 'storage.dart';

//TODO refactor
class SettingsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          leading: BackButton(
            onPressed: () => Navigator.of(context).pushNamed('/main'),
          ),
          title: Text("Settings"),
          actions: <Widget>[buildPopUpMenu(context)]),
      body: buildForm(SettingsWidget()),
    );
  }
}

PopupMenuButton buildPopUpMenu(BuildContext context) {
  return PopupMenuButton<String>(
    onSelected: (String value) {
      session.post('logout').catchError((_) {});
      session.clearSession();
      Navigator.of(context).pushNamed('/login');
    },
    itemBuilder: (BuildContext context) {
      return [PopupMenuItem<String>(value: "Logout", child: Text("Logout"))];
    },
  );
}

class SettingsWidget extends StatefulWidget {
  @override
  _SettingsState createState() => _SettingsState();
}

class _SettingsState extends State<SettingsWidget> {
  final _controllers = {
    "name": TextEditingController(text: storage.name),
    "old_pass": TextEditingController(),
    "new_pass": TextEditingController(),
    "new_pass2": TextEditingController(),
  };
  final _formKey = GlobalKey<FormState>();
  bool _exiting = false;

  // TODO use loading screen
  void _sendRequest() {
    if (this._formKey.currentState.validate()) {
      Map<String, String> fields = {};
      fields['name'] = this._controllers["name"].value.text;
      if (this._controllers["new_pass"].value.text != '') {
        fields['new_pass'] = this._controllers["new_pass"].value.text;
        fields['old_pass'] = this._controllers["old_pass"].value.text;
      }
      session
          .post('edit_user', jsonEncode(fields))
          .then(this._processResponse)
          .catchError((err) {
        displayError(context, "Connection error ${err.toString()}");
      });
    }
  }

  void _processResponse(http.Response response) {
    if (response.statusCode != 200) {
      displayError(context, "Problem with connection.");
      return;
    }
    Map<String, dynamic> responseBody = jsonDecode(response.body);
    if (responseBody['status'] == 'incomplete user data') {
      displayError(context, "Error with the request body.");
      return;
    }
    if (responseBody['status'] == 'invalid pass') {
      displayError(context, "Invalid password.");
      return;
    }
    if (responseBody['status'] == 'OK') {
      // TODO show result
    }
    if (this._exiting) {
      this._exiting = false;
      Navigator.of(context).pushNamed('/main');
    }
  }

  void _applyAndExit() {
    this._exiting = true;
    _sendRequest();
  }

  String _validateSecondPassword(String value) {
    if (value != this._controllers["new_pass"].value.text) {
      return "Passwords must be identical";
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Form(
        key: this._formKey,
        child: Column(mainAxisSize: MainAxisSize.min, children: <Widget>[
          Text("Change name:", style: Theme.of(context).textTheme.headline6),
          buildTextField(this._controllers["name"], "Name"),
          Text("Change password:",
              style: Theme.of(context).textTheme.headline6),
          buildTextField(this._controllers["old_pass"], "Current password",
              obscure: true),
          buildTextField(this._controllers["new_pass"], "New password",
              obscure: true),
          buildValidatedTextField(this._controllers["new_pass2"],
              "Repeat new password", this._validateSecondPassword,
              obscure: true),
          ButtonBar(
            alignment: MainAxisAlignment.center,
            children: [
              buildButton("Apply", this._sendRequest),
              buildButton("Apply & return", this._applyAndExit)
            ],
          )
        ]));
  }
}
