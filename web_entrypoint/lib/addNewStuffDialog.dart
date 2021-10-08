import 'package:flutter/material.dart';

import 'common.dart';
import 'datefield.dart';

void Function() addNewEventDialogMethod(BuildContext context) {
  return () {
    var diffController = TextEditingController();
    var dateField = DateField();
    var descriptionController = TextEditingController();
    showDialog(
        context: context,
        builder: (BuildContext context) => AlertDialog(
              title: const Text('Add new event'),
              content: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    buildIntField(diffController, "diff"),
                    dateField,
                    buildTextField(descriptionController, "description")
                  ]),
              actions: <Widget>[
                buildButton("Create", () {
                  Navigator.pushNamed(context, "/loading",
                      arguments: LoadingArgs(LoadingType.CREATE_EVENT,
                          diff: int.parse(diffController.value.text),
                          dateTime: DateTime.now(),
                          description: descriptionController.value.text));
                }),
                buildButton("Cancel", () {
                  Navigator.pop(context, 'Cancel');
                })
              ],
            ));
  };
}
