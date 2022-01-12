import 'package:flutter/material.dart';

import 'widgets/app_bar.dart';
import 'widgets/common/element_list.dart';
import 'widgets/common/common.dart';
import 'widgets/account_dialog.dart';
import 'widgets/drawer.dart';

import '../storage.dart';

class AccountListView extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _AccountListViewState();
}

class _AccountListViewState extends State<AccountListView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: buildAppBar(context),
        body: buildForm(AccountList()),
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
  Widget buildListElement(BuildContext context, var account) {
    Function onEdit = editAccountDialogMethod(context, account);
    Function onRemove = removeAccountDialogMethod(context, account);
    return buildListElementBase(Text(account['name']), onEdit, onRemove);
  }
}

// class _AccountListState extends State<AccountList> {
// //TODO remove Add account button when limit is reached
//   Null Function(int) changeAccountMethod(BuildContext context) {
//     return (int accountIndex) {
//       if (accountIndex == -1) {
//         showCreateAccountDialog(context);
//       } else {
//         setState(() {
//           storage.accountIndex = accountIndex;
//           Navigator.pushNamed(context, "/loading",
//               arguments: LoadingArgs(LoadingType.SYNC_DATA));
//         });
//       }
//     };
//   }

//   @override
//   Widget build(BuildContext context) {
//     List<DropdownMenuItem<int>> items = [];
//     for (int i = 0; i < storage.accounts.length; i++) {
//       var account = storage.accounts[i];
//       items.add(buildAccountButton(i, account));
//     }
//     items.add(
//         DropdownMenuItem<int>(child: Text("+ Add new account"), value: -1));
//     return DropdownButton<int>(
//       value: storage.accountIndex,
//       items: items,
//       onChanged: changeAccountMethod(context),
//     );
//   }
