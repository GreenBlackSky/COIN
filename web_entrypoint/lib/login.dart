import 'package:flutter/material.dart';

import 'common.dart';

class LogInScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(leading: new Container(), title: Text("COIN")),
        backgroundColor: Colors.grey[200],
        body: buildForm(LogInForm()));
  }
}

class LogInForm extends StatefulWidget {
  @override
  _LogInFormState createState() => _LogInFormState();
}

class _LogInFormState extends State<LogInForm> {
  final _nameController = TextEditingController();
  final _passController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  void _login() {
    if (_formKey.currentState.validate()) {
      Navigator.pushNamed(context, "/loading",
          arguments: UserArgs(false, this._nameController.value.text,
              this._passController.value.text));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          Text('Log in', style: Theme.of(context).textTheme.headline4),
          buildTextField(_nameController, "Name"),
          buildTextField(_passController, "Password", obscure: true),
          ButtonBar(alignment: MainAxisAlignment.spaceEvenly, children: [
            buildButton("Log in", _login),
            buildButton("Don't have an account", () {
              Navigator.of(context).pushNamed('/signup');
            })
          ])
        ],
      ),
    );
  }
}
