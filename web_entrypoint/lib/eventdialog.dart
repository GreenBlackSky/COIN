import 'package:flutter/material.dart';

import 'common.dart';
import 'datefield.dart';

void Function() _eventDialog(
  BuildContext context,
  String title,
  String buttonText,
  LoadingType action,
  int eventID,
  int diff,
  DateTime eventTime,
  String description,
) {
  return () {
    var diffController = TextEditingController(text: diff.toString());
    var dateField = DateField(eventTime);
    var descriptionController = TextEditingController(text: description);
    showDialog(
        context: context,
        builder: (BuildContext context) => AlertDialog(
              title: Text(title),
              content: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    buildIntField(diffController, "diff"),
                    dateField,
                    buildTextField(descriptionController, "description")
                  ]),
              actions: <Widget>[
                buildButton(buttonText, () {
                  Navigator.pushNamed(context, "/loading",
                      arguments: LoadingArgs(action,
                          id: eventID,
                          diff: int.parse(diffController.value.text),
                          dateTime: dateField.selectedDate,
                          description: descriptionController.value.text));
                }),
                buildButton("Cancel", () {
                  Navigator.pop(context, 'Cancel');
                })
              ],
            ));
  };
}

void Function() addNewEventDialogMethod(BuildContext context) {
  return _eventDialog(context, "Add new event", "Create",
      LoadingType.CREATE_EVENT, -1, 0, DateTime.now(), "");
}

void Function() editEventDialogMethod(
    BuildContext context, Map<String, dynamic> event) {
  return _eventDialog(
      context,
      "Edit event",
      "Edit",
      LoadingType.EDIT_EVENT,
      event['id'],
      event["diff"],
      DateTime.fromMillisecondsSinceEpoch(event["event_time"] * 1000),
      event["description"]);
}
