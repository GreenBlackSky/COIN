import 'package:flutter/material.dart';

import 'common/common.dart';
import 'common/text_fields.dart';
import '../../network/session.dart';
import '../../storage.dart';

//TODO switch themes
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

  void _sendRequest(bool exiting) {
    if (this._formKey.currentState.validate()) {
      Navigator.pushNamed(context, "/loading",
          arguments: LoadingArgs(LoadingType.EDIT_USER,
              name: this._controllers["name"].value.text,
              password: this._controllers["old_pass"].value.text,
              newPassword: this._controllers["new_pass"].value.text,
              endpoint: (exiting ? "/main" : "/settings")));
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
          ButtonBar(
            alignment: MainAxisAlignment.center,
            children: [
              buildButton("Apply", () {
                this._sendRequest(false);
              }),
              buildButton("Apply & return", () {
                this._sendRequest(true);
              })
            ],
          )
        ]));
  }
}
