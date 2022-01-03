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
    return (int accountID) {
      if (accountID == -1) {
        showCreateAccountDialog(context);
      } else {
        setState(() {
          storage.account = accountID;
          Navigator.pushNamed(context, "/loading",
              arguments: LoadingArgs(LoadingType.SYNC_DATA));
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
          onPressed: () {
            return showRenameAccountDialog(context, accountID);
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
                  LoadingArgs(LoadingType.DELETE_ACCOUNT, id: accountID));
        }),
      ));
    }
    return DropdownMenuItem<int>(
        value: accountID,
        child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [Text(accountName), Row(children: buttons)]));
  }
}
