import 'package:flutter/material.dart';

import 'common/common.dart';
import 'common/confirmation_dialog.dart';
import 'common/datefield.dart';
import 'common/text_fields.dart';

import 'package:coin_client/storage.dart';
import 'package:coin_client/common.dart';

class CategoryComboBox extends StatefulWidget {
  CategoryComboBox(this.selectedCategoryId);
  int selectedCategoryId;
  @override
  _CategoryComboBox createState() {
    return _CategoryComboBox();
  }
}

class _CategoryComboBox extends State<CategoryComboBox> {
  @override
  Widget build(BuildContext context) {
    var category = storage.categories.where((element) {
      return element['id'] == widget.selectedCategoryId;
    }).first;
    return DropdownButton<int>(
        value: category['id'],
        icon: const Icon(Icons.arrow_downward),
        elevation: 16,
        underline: Container(
          height: 2,
          color: category['color'],
        ),
        onChanged: (int newValue) {
          widget.selectedCategoryId = newValue;
        },
        items: storage.categories.map<DropdownMenuItem<int>>((var category) {
          return DropdownMenuItem<int>(
            value: category['id'],
            child: Text(category['name']),
          );
        }).toList());
  }
}

void Function() baseEventDialog(
    BuildContext context,
    String title,
    String buttonText,
    LoadingType action,
    int eventID,
    int diff,
    DateTime eventTime,
    String description,
    int categoryID) {
  return () {
    var diffController = TextEditingController(text: diff.toString());
    var dateField = DateField(eventTime);
    var categoryComboBox = CategoryComboBox(categoryID);
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
                    buildTextField(descriptionController, "description"),
                    categoryComboBox,
                  ]),
              actions: <Widget>[
                buildButton(buttonText, () {
                  Navigator.pushNamed(context, "/loading",
                      arguments: LoadingArgs(action,
                          id: eventID,
                          id2: categoryComboBox.selectedCategoryId,
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
  return baseEventDialog(
      context,
      "Add new event",
      "Create",
      LoadingType.CREATE_EVENT,
      -1,
      0,
      DateTime.now(),
      "",
      storage.categories[0]['id']);
}

void Function() editEventDialogMethod(
    BuildContext context, Map<String, dynamic> event) {
  return baseEventDialog(
      context,
      "Edit event",
      "Edit",
      LoadingType.EDIT_EVENT,
      event['id'],
      event["diff"],
      dateFromTimestamp(event["event_time"]),
      event["description"],
      event['category_id']);
}

void Function() deleteEventDialogMethod(
    BuildContext context, Map<String, dynamic> event) {
  return confirmDialogMethod(
    context,
    "Are you sure you want to delete event?",
    "Delete event",
    () {
      Navigator.pushNamed(context, "/loading",
          arguments: LoadingArgs(LoadingType.DELETE_EVENT, id: event["id"]));
    },
  );
}
