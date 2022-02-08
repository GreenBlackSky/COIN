import 'package:flutter/material.dart';

Widget buildForm(Widget widget) {
  return Center(
    child: SizedBox(
      width: 400,
      child: Card(
        child: widget,
      ),
    ),
  );
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
  final int id2;
  final int id3;
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
      this.id2 = -1,
      this.id3 = -1,
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
