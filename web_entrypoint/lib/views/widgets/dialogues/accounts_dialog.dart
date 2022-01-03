import 'package:flutter/material.dart';

import '../common/common.dart';
import '../common/text_fields.dart';
import '../../../storage.dart';

Future<String> _accountDialog(BuildContext context, String title, String hint,
    String buttonText, LoadingType action,
    {int id = -1, String accountName = ""}) {
  var controller = TextEditingController(text: accountName);
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
}

Future<String> showCreateAccountDialog(BuildContext context) {
  return _accountDialog(
    context,
    "Create new account",
    "New account name",
    "Create",
    LoadingType.CREATE_ACCOUNT,
  );
}

Future<String> showRenameAccountDialog(BuildContext context, int accountID) {
  return _accountDialog(context, "Rename account", "New account name", "Rename",
      LoadingType.EDIT_ACCOUNT,
      id: accountID, accountName: storage.accounts[accountID]);
}
