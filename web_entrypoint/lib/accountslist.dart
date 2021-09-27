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

  @override
  Widget build(BuildContext context) {
    return DropdownButton<int>(
      value: storage.account,
      items: [
            for (MapEntry e in storage.accounts.entries)
              DropdownMenuItem<int>(child: Text(e.value), value: e.key)
          ] +
          [DropdownMenuItem<int>(child: Text("+ Add new account"), value: -1)],
      onChanged: changeAccountMethod(context),
    );
  }
}
