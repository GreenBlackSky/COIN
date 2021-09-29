import 'package:flutter/material.dart';

import 'storage.dart';
import 'common.dart';

class AccountList extends StatefulWidget {
  const AccountList({Key key}) : super(key: key);

  @override
  State<AccountList> createState() => _AccountListState();
}

class _AccountListState extends State<AccountList> {
  String dropdownValue = 'One';
//TODO remove delete button on last account
//TODO remove Add account button when limit is reached
//TODO colors
//TODO refactor
  Null Function(int) changeAccountMethod(BuildContext context) {
    return (int accountID) {
      if (accountID == -1) {
        showCreateAccountDialog();
      } else {
        setState(() {
          storage.account = accountID;
        });
      }
    };
  }

  Null Function() deleteAccountMethod(int accountID) {
    return () {
      Navigator.pushNamed(context, "/loading",
          arguments: LoadingArgs(LoadingType.DELETE_ACCOUNT, id: accountID));
    };
  }

  @override
  Widget build(BuildContext context) {
    return DropdownButton<int>(
      value: storage.account,
      items: [
            for (MapEntry e in storage.accounts.entries)
              buildAccountButton(e.key, e.value)
          ] +
          [DropdownMenuItem<int>(child: Text("+ Add new account"), value: -1)],
      onChanged: changeAccountMethod(context),
    );
  }

  DropdownMenuItem<int> buildAccountButton(int accountID, String accountName) {
    return DropdownMenuItem<int>(
        value: accountID,
        child: Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
          Text(accountName),
          Row(children: [
            IconButton(
                icon: Icon(Icons.edit),
                color: Colors.black,
                onPressed: showRenameAccountDialogMethod(accountID)),
            IconButton(
              icon: Icon(Icons.delete),
              color: Colors.black,
              onPressed: deleteAccountMethod(accountID),
            )
          ])
        ]));
  }

  Future<String> Function() showRenameAccountDialogMethod(int accountID) {
    return () {
      var controller = TextEditingController();
      return showDialog<String>(
          context: context,
          builder: (BuildContext context) => AlertDialog(
                title: const Text('Rename account'),
                content: buildTextField(controller, "New name"),
                actions: <Widget>[
                  TextButton(
                    child: const Text('Rename'),
                    onPressed: () {
                      Navigator.pushNamed(context, "/loading",
                          arguments: LoadingArgs(LoadingType.EDIT_ACCOUNT,
                              name: controller.value.text, id: accountID));
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

  Future<String> showCreateAccountDialog() {
    var controller = TextEditingController();
    return showDialog<String>(
        context: context,
        builder: (BuildContext context) => AlertDialog(
              title: const Text('Create new account'),
              content: buildTextField(controller, "New account name"),
              actions: <Widget>[
                TextButton(
                  child: const Text('Create'),
                  onPressed: () {
                    Navigator.pushNamed(context, "/loading",
                        arguments: LoadingArgs(LoadingType.CREATE_ACCOUNT,
                            name: controller.value.text));
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
}
