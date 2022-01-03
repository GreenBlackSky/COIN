import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

Widget buildForm(StatefulWidget widget) {
  return Center(
    child: SizedBox(
      width: 400,
      child: Card(
        child: widget,
      ),
    ),
  );
}

Widget _buildTextFieldImpl(TextEditingController controller, String hint,
    Function validator, bool obscure, List formatters) {
  return Padding(
    padding: EdgeInsets.all(8.0),
    child: TextFormField(
      inputFormatters: formatters,
      controller: controller,
      decoration: InputDecoration(
        focusedBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Colors.blueAccent, width: 3.0),
        ),
        enabledBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Colors.grey, width: 3.0),
        ),
        hintText: hint,
      ),
      validator: validator,
      obscureText: obscure,
    ),
  );
}

Widget buildIntField(TextEditingController controller, String hint,
    {bool obscure = false}) {
  return _buildTextFieldImpl(controller, hint, (value) => null, obscure,
      <TextInputFormatter>[FilteringTextInputFormatter.digitsOnly]);
}

Widget buildTextField(TextEditingController controller, String hint,
    {bool obscure = false}) {
  return _buildTextFieldImpl(
      controller, hint, (value) => null, obscure, <TextInputFormatter>[]);
}

Widget buildValidatedTextField(
    TextEditingController controller, String hint, Function validator,
    {bool obscure = false}) {
  if (validator == null) {
    validator = (value) {
      if (value.isEmpty) {
        return "Please enter $hint";
      }
      return null;
    };
  }
  return _buildTextFieldImpl(
      controller, hint, validator, obscure, <TextInputFormatter>[]);
}

Widget buildButton(String text, Function callback) {
  return Padding(
    padding: EdgeInsets.all(8.0),
    child: TextButton(
      style: ButtonStyle(
        foregroundColor:
            MaterialStateColor.resolveWith((Set<MaterialState> states) {
          return states.contains(MaterialState.disabled) ? null : Colors.white;
        }),
        backgroundColor:
            MaterialStateColor.resolveWith((Set<MaterialState> states) {
          return states.contains(MaterialState.disabled) ? null : Colors.blue;
        }),
      ),
      onPressed: callback,
      child: Text(text),
    ),
  );
}

void displayError(BuildContext context, String text) {
  final bar = SnackBar(
    content: Text(text),
  );
  ScaffoldMessenger.of(context).showSnackBar(bar);
}

DateTime dateFromTimestamp(int timestamp) {
  return DateTime.fromMillisecondsSinceEpoch(timestamp * 1000);
}

int timestampFromDateTime(DateTime dateTime) {
  return dateTime.millisecondsSinceEpoch ~/ 1000;
}

String dateToString(DateTime date) {
  return "${date.day}/${date.month}/${date.year}";
}

String timestampToString(int timestamp) {
  var date = dateFromTimestamp(timestamp);
  return "${date.day}/${date.month}/${date.year}";
}

enum LoadingType {
  REGISTER,
  LOGIN,
  EDIT_USER,
  CREATE_ACCOUNT,
  EDIT_ACCOUNT,
  DELETE_ACCOUNT,
  CREATE_CATEGORY,
  EDIT_CATEGORY,
  DELETE_CATEGORY,
  SYNC_DATA,
  CREATE_EVENT,
  EDIT_EVENT,
  DELETE_EVENT
}

class LoadingArgs {
  final LoadingType type;
  final String name;
  final String password;
  final String newPassword;
  final int id;
  final int diff;
  final DateTime dateTime;
  final DateTime startTime;
  final DateTime endTime;
  final String description;
  final String endpoint;
  final Color color;

  LoadingArgs(this.type,
      {this.name = "",
      this.password = "",
      this.newPassword = "",
      this.id = -1,
      this.diff = 0,
      DateTime dateTime,
      DateTime startTime,
      DateTime endTime,
      this.description = '',
      this.endpoint = '',
      this.color = Colors.black})
      : this.dateTime = dateTime ?? DateTime.now(),
        this.startTime = startTime ?? DateTime.now(),
        this.endTime = endTime ?? DateTime.now();
}
