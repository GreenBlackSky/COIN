import 'package:flutter/material.dart';

import 'common/common.dart';
import 'common/confirmation_dialog.dart';
import 'dialogues/accounts_dialog.dart';
import '../../storage.dart';

class AccountList extends StatefulWidget {
  const AccountList({Key key}) : super(key: key);

  @override
  State<AccountList> createState() => _AccountListState();
}

class _AccountListState extends State<AccountList> {
//TODO remove Add account button when limit is reached
  Null Function(int) changeAccountMethod(BuildContext context) {
    return (int accountIndex) {
      if (accountIndex == -1) {
        showCreateAccountDialog(context);
      } else {
        setState(() {
          storage.accountIndex = accountIndex;
          Navigator.pushNamed(context, "/loading",
              arguments: LoadingArgs(LoadingType.SYNC_DATA));
        });
      }
    };
  }

  @override
  Widget build(BuildContext context) {
    List<DropdownMenuItem<int>> items = [];
    for (int i = 0; i < storage.accounts.length; i++) {
      var account = storage.accounts[i];
      items.add(buildAccountButton(i, account));
    }
    items.add(
        DropdownMenuItem<int>(child: Text("+ Add new account"), value: -1));
    return DropdownButton<int>(
      value: storage.accountIndex,
      items: items,
      onChanged: changeAccountMethod(context),
    );
  }

  DropdownMenuItem<int> buildAccountButton(int index, var account) {
    var buttons = [
      IconButton(
          icon: Icon(Icons.edit),
          color: Colors.black,
          onPressed: () {
            return showRenameAccountDialog(context, account);
          }),
    ];
    if (storage.accounts.length != 1) {
      buttons.add(IconButton(
        icon: Icon(Icons.delete),
        color: Colors.black,
        onPressed: confirmDialogMethod(context,
            "Are you sure you want to delete account?", "Delete account", () {
          Navigator.pushNamed(context, "/loading",
              arguments:
                  LoadingArgs(LoadingType.DELETE_ACCOUNT, id: account['id']));
        }),
      ));
    }
    return DropdownMenuItem<int>(
        value: index,
        child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [Text(account['name']), Row(children: buttons)]));
  }
}
