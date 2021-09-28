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
//TODO enter new account name
//TODO edit account name
//TODO remove delete button on last account
//TODO remove Add account button when limit is reached
//TODO colors
  Null Function(int) changeAccountMethod(BuildContext context) {
    return (int accountID) {
      if (accountID == -1) {
        Navigator.pushNamed(context, "/loading",
            arguments:
                LoadingArgs(LoadingType.CREATE_ACCOUNT, name: "NEW ACCOUNT"));
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
          arguments:
              LoadingArgs(LoadingType.DELETE_ACCOUNT, accountID: accountID));
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
              onPressed: () {},
            ),
            IconButton(
              icon: Icon(Icons.delete),
              color: Colors.black,
              onPressed: deleteAccountMethod(accountID),
            )
          ])
        ]));
  }
}
