import 'package:flutter/material.dart';

import 'storage.dart';
import 'common.dart';

class AccountList extends StatefulWidget {
  const AccountList({Key key}) : super(key: key);

  @override
  State<AccountList> createState() => _AccountListState();
}

class _AccountListState extends State<AccountList> {
//TODO remove Add account button when limit is reached
//TODO refactor
//TODO try Expanded Text on button
  Null Function(int) changeAccountMethod(BuildContext context) {
    return (int accountID) {
      if (accountID == -1) {
        showCreateAccountDialog();
      } else {
        setState(() {
          storage.account = accountID;
          Navigator.pushNamed(context, "/loading",
              arguments: LoadingArgs(LoadingType.GET_EVENTS));
        });
      }
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
    var buttons = [
      IconButton(
          icon: Icon(Icons.edit),
          color: Colors.black,
          onPressed: showRenameAccountDialogMethod(accountID)),
    ];
    if (storage.accounts.length != 1) {
      buttons.add(IconButton(
        icon: Icon(Icons.delete),
        color: Colors.black,
        onPressed: showDeleteAccountDialogMethod(accountID),
      ));
    }
    return DropdownMenuItem<int>(
        value: accountID,
        child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [Text(accountName), Row(children: buttons)]));
  }

  Future<String> showCreateAccountDialog() {
    var controller = TextEditingController();
    return showDialog<String>(
        context: this.context,
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

  Future<String> Function() showRenameAccountDialogMethod(int accountID) {
    return () {
      var controller = TextEditingController();
      return showDialog<String>(
          context: this.context,
          builder: (BuildContext context) => AlertDialog(
                title: const Text('Rename account'),
                content:
                    buildTextField(controller, storage.accounts[accountID]),
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

  Future<String> Function() showDeleteAccountDialogMethod(int accountID) {
    return () {
      return showDialog<String>(
          context: this.context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text('Are you sure you want to delete account?'),
              actions: <Widget>[
                TextButton(
                  child: const Text('Delete account'),
                  onPressed: () {
                    Navigator.pushNamed(context, "/loading",
                        arguments: LoadingArgs(LoadingType.DELETE_ACCOUNT,
                            id: accountID));
                  },
                ),
                TextButton(
                  child: const Text('Cancel'),
                  onPressed: () {
                    Navigator.pop(context, 'Cancel');
                  },
                ),
              ],
            );
          });
    };
  }
}
