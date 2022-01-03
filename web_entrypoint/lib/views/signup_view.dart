import 'package:flutter/material.dart';

import 'widgets/common/common.dart';
import 'widgets/common/text_fields.dart';

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
          arguments: LoadingArgs(LoadingType.REGISTER,
              name: this._nameController.value.text,
              password: this._passController1.value.text));
    }
  }

  String _validateSecondPassword(String value) {
    if (value.isEmpty) {
      return "Please enter password";
    }
    if (value != this._passController1.value.text) {
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
          buildTextField(this._nameController, "Name"),
          buildTextField(this._passController1, "Password", obscure: true),
          buildValidatedTextField(
              this._passController2, "Repeat password", _validateSecondPassword,
              obscure: true),
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
