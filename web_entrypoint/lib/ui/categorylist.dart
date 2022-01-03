import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

import '../storage.dart';
import 'common_widgets/confirmation_dialog.dart';
import 'common_widgets/elements_list.dart';
import 'common_widgets/list_element.dart';
import 'common_widgets/common.dart';
import 'common_widgets/text_fields.dart';

void Function() _categoryDialog(
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
  return _categoryDialog(context, "Add new category", "Create",
      LoadingType.CREATE_CATEGORY, -1, '', Colors.orange);
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

class CategoryList extends ElementsList {
  final elements = storage.categories;

  @override
  Widget buildListElement(BuildContext context, var category) {
    Function onEdit = editCategoryDialogMethod(context, category);
    Function onRemove = confirmDialogMethod(
      context,
      "Are you sure you want to delete event?",
      "Delete event",
      () {
        Navigator.pushNamed(context, "/loading",
            arguments:
                LoadingArgs(LoadingType.DELETE_CATEGORY, id: category["id"]));
      },
    );
    return buildListElementBase(category['name'], onEdit, onRemove,
        color: category['color']);
  }
}
