import 'package:flutter/material.dart';

import 'widgets/common/common.dart';
import 'widgets/common/text_fields.dart';
import 'widgets/drawer.dart';

import '../network/session.dart';
import '../storage.dart';

//TODO switch themes
class SettingsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Settings")),
      drawer: buildDrawer(context),
      body: buildForm(SettingsWidget()),
    );
  }
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

  void _sendRequest() {
    if (this._formKey.currentState.validate()) {
      Navigator.pushNamed(context, "/loading",
          arguments: LoadingArgs(LoadingType.EDIT_USER,
              name: this._controllers["name"].value.text,
              password: this._controllers["old_pass"].value.text,
              newPassword: this._controllers["new_pass"].value.text,
              endpoint: "/settings"));
    }
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
          buildButton("Apply", () {
            this._sendRequest();
          })
        ]));
  }
}
