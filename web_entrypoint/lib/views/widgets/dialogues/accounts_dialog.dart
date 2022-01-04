import 'package:flutter/material.dart';

import '../common/common.dart';
import '../common/text_fields.dart';

Future<String> Function() baseAccountDialog(BuildContext context, String title,
    String hint, String buttonText, LoadingType action,
    {int id = -1, String accountName = ""}) {
  var controller = TextEditingController(text: accountName);
  return () {
    return showDialog<String>(
        context: context,
        builder: (BuildContext context) => AlertDialog(
              title: Text(title),
              content: buildTextField(controller, hint),
              actions: <Widget>[
                TextButton(
                  child: Text(buttonText),
                  onPressed: () {
                    Navigator.pushNamed(context, "/loading",
                        arguments: LoadingArgs(action,
                            name: controller.value.text, id: id));
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
