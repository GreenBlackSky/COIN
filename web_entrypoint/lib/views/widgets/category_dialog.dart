import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

import 'common/common.dart';
import 'common/text_fields.dart';
import 'common/confirmation_dialog.dart';

void Function() baseCategoryDialog(
    BuildContext context,
    String title,
    String buttonText,
    LoadingType action,
    int categoryID,
    String name,
    Color color) {
  return () {
    var nameController = TextEditingController(text: name);
    Color chosenColor = color;
    showDialog(
        context: context,
        builder: (BuildContext context) => AlertDialog(
              title: Text(title),
              content: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    buildTextField(nameController, "Category name"),
                    BlockPicker(
                        pickerColor: color,
                        onColorChanged: (Color newColor) {
                          chosenColor = newColor;
                        })
                  ]),
              actions: <Widget>[
                buildButton(buttonText, () {
                  Navigator.pushNamed(context, "/loading",
                      arguments: LoadingArgs(action,
                          id: categoryID,
                          name: nameController.value.text,
                          color: chosenColor));
                }),
                buildButton("Cancel", () {
                  Navigator.pop(context, 'Cancel');
                })
              ],
            ));
  };
}

void Function() addNewCategoryDialogMethod(BuildContext context) {
  return baseCategoryDialog(context, "Add new category", "Create",
      LoadingType.CREATE_CATEGORY, -1, '', Colors.orange);
}

void Function() editCategoryDialogMethod(
    BuildContext context, Map<String, dynamic> category) {
  return baseCategoryDialog(
      context,
      "Edit category",
      "Edit",
      LoadingType.EDIT_CATEGORY,
      category['id'],
      category['name'],
      category['color']);
}

void Function() deleteCategoryDialogMethod(
    BuildContext context, Map<String, dynamic> category) {
  return confirmDialogMethod(
    context,
    "Are you sure you want to delete category?",
    "Delete category",
    () {
      Navigator.pushNamed(context, "/loading",
          arguments:
              LoadingArgs(LoadingType.DELETE_CATEGORY, id: category["id"]));
    },
  );
}
