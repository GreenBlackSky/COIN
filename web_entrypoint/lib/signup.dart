import 'package:flutter/material.dart';

import 'common.dart';

class SignUpScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(leading: new Container(), title: Text("COIN")),
        backgroundColor: Colors.grey[200],
        body: buildForm(SignUpForm()));
  }
}

class SignUpForm extends StatefulWidget {
  @override
  _SignUpFormState createState() => _SignUpFormState();
}

class _SignUpFormState extends State<SignUpForm> {
  final _nameController = TextEditingController();
  final _passController1 = TextEditingController();
  final _passController2 = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  void _signup() {
    if (_formKey.currentState.validate()) {
      Navigator.pushNamed(context, "/loading",
          arguments: UserArgs(true, this._nameController.value.text,
              this._passController1.value.text));
    }
  }

  String _validateSecondPassword(String value) {
    if (value.isEmpty) {
      return "Please enter password";
    }
    if (value != _passController1.value.text) {
      return "Passwords must be identical";
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          Text('Sign up', style: Theme.of(context).textTheme.headline4),
          buildTextField(_nameController, "Name"),
          buildTextField(_passController1, "Password", obscure: true),
          buildTextField(_passController2, "Repeat password",
              validator: _validateSecondPassword, obscure: true),
          ButtonBar(alignment: MainAxisAlignment.spaceEvenly, children: [
            buildButton("Sign up", _signup),
            buildButton("Already have an account", () {
              Navigator.of(context).pushReplacementNamed('/login');
            })
          ])
        ],
      ),
    );
  }
}
