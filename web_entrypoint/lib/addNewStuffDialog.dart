import 'package:flutter/material.dart';

import 'common.dart';

void Function() addNewEventDialogMethod(BuildContext context) {
  return () {
    var diffController = TextEditingController();
    var timeController = TextEditingController();
    var descriptionController = TextEditingController();
    showDialog(
        context: context,
        builder: (BuildContext context) => AlertDialog(
              title: const Text('Add new event'),
              content: Column(children: [
                buildTextField(diffController, "diff"), //TODO validate
                buildTextField(timeController, "time"), //TODO datetime picker
                buildTextField(descriptionController, "description")
              ]),
              actions: <Widget>[
                TextButton(
                  child: const Text('Create'),
                  onPressed: () {
                    Navigator.pushNamed(context, "/loading",
                        arguments: LoadingArgs(LoadingType.CREATE_EVENT,
                            diff: int.parse(diffController.value.text),
                            dateTime: DateTime.parse(timeController.value.text),
                            description: descriptionController.value.text));
                  },
                ),
                TextButton(
                  child: const Text('Cancel'),
                  onPressed: () {
                    Navigator.pop(context, 'Cancel');
                  },
                ),
              ],
            ));
  };
}
