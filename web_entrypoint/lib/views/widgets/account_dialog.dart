import 'package:flutter/material.dart';

import 'common/common.dart';
import 'common/text_fields.dart';
import 'common/confirmation_dialog.dart';

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

void Function() addNewAccountDialogMethod(BuildContext context) {
  return baseAccountDialog(
    context,
    "Create new account",
    "New account name",
    "Create",
    LoadingType.CREATE_ACCOUNT,
  );
}

void Function() editAccountDialogMethod(BuildContext context, var account) {
  return baseAccountDialog(context, "Rename account", "New account name",
      "Rename", LoadingType.EDIT_ACCOUNT,
      id: account['id'], accountName: account['name']);
}

void Function() removeAccountDialogMethod(BuildContext context, var account) {
  return confirmDialogMethod(
      context, "Are you sure you want to delete account?", "Delete account",
      () {
    Navigator.pushNamed(context, "/loading",
        arguments: LoadingArgs(LoadingType.DELETE_ACCOUNT, id: account['id']));
  });
}
