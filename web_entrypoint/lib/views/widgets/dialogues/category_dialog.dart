import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

import '../common/common.dart';
import '../common/text_fields.dart';

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
