import 'package:flutter/material.dart';

import 'widgets/account_dialog.dart';
import 'widgets/common/common.dart';
import 'widgets/common/confirmation_dialog.dart';
import 'widgets/common/element_list.dart';
import 'widgets/drawer.dart';
import 'widgets/topper.dart';

import 'package:coin_client/storage.dart';

class AccountListView extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _AccountListViewState();
}

class _AccountListViewState extends State<AccountListView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: Topper(context),
        body: buildForm(AccountList(), 0.3),
        drawer: buildDrawer(context),
        floatingActionButton: FloatingActionButton(
            onPressed: addNewAccountDialogMethod(context),
            child: Icon(Icons.add),
            tooltip: "Add new account"));
  }
}

class AccountList extends ElementsList {
  final elements = storage.accounts;

  @override
  Widget buildListElement(BuildContext context, var account, int index) {
    void Function() onEdit = editAccountDialogMethod(context, account);
    void Function() onRemove;
    if (storage.accounts.length > 1) {
      onRemove = removeAccountDialogMethod(context, account);
    }
    void Function() switchAccount;
    if (index != storage.accountIndex) {
      switchAccount = confirmDialogMethod(
          context, "Are you sure you want to switch account?", "Switch", () {
        storage.accountIndex = index;
        Navigator.pushNamed(context, "/loading",
            arguments: LoadingArgs(LoadingType.SYNC_DATA));
      });
    }
    return ElevatedButton(
      child: buildListElementBase(Text(account['name']), onEdit, onRemove),
      onPressed: switchAccount,
    );
  }
}
