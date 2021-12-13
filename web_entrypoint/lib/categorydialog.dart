import 'package:flutter/material.dart';

import 'common.dart';

void Function() _categoryDialog(
    BuildContext context,
    String title,
    String buttonText,
    LoadingType action,
    int categoryID,
    String name,
    String color) {
  return () {
    var nameController = TextEditingController(text: name);
    var colorController = TextEditingController(text: color);
    showDialog(
        context: context,
        builder: (BuildContext context) => AlertDialog(
              title: Text(title),
              content: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    buildTextField(nameController, "Category name"),
                    buildTextField(colorController, "Category color")
                  ]),
              actions: <Widget>[
                buildButton(buttonText, () {
                  Navigator.pushNamed(context, "/loading",
                      arguments: LoadingArgs(action,
                          id: categoryID, name: name, color: color));
                }),
                buildButton("Cancel", () {
                  Navigator.pop(context, 'Cancel');
                })
              ],
            ));
  };
}

void Function() addNewCategoryDialogMethod(BuildContext context) {
  return _categoryDialog(context, "Add new category", "Create",
      LoadingType.CREATE_CATEGORY, -1, '', '');
}

void Function() editCategoryDialogMethod(
    BuildContext context, Map<String, dynamic> category) {
  return _categoryDialog(
      context,
      "Edit category",
      "Edit",
      LoadingType.EDIT_CATEGORY,
      category['id'],
      category['name'],
      category['color']);
}
