import 'package:flutter/material.dart';

import 'common/common.dart';
import 'common/confirmation_dialog.dart';
import 'common/elements_list.dart';
import 'dialogues/accounts_dialog.dart';
import '../../storage.dart';

void Function() showCreateAccountDialog(BuildContext context) {
  return baseAccountDialog(
    context,
    "Create new account",
    "New account name",
    "Create",
    LoadingType.CREATE_ACCOUNT,
  );
}

void Function() showRenameAccountDialog(BuildContext context, var account) {
  return baseAccountDialog(context, "Rename account", "New account name",
      "Rename", LoadingType.EDIT_ACCOUNT,
      id: account['id'], accountName: account['name']);
}

void Function() showRemoveAccountDialog(BuildContext context, var account) {
  return confirmDialogMethod(
      context, "Are you sure you want to delete account?", "Delete account",
      () {
    Navigator.pushNamed(context, "/loading",
        arguments: LoadingArgs(LoadingType.DELETE_ACCOUNT, id: account['id']));
  });
}

class AccountList extends ElementsList {
  final elements = storage.accounts;

  @override
  Widget buildListElement(BuildContext context, var account) {
    Function onEdit = showRenameAccountDialog(context, account);
    Function onRemove = showRemoveAccountDialog(context, account);
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
