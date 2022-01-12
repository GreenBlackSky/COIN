import 'package:flutter/material.dart';

import '../../storage.dart';

Widget buildAppBar(context) {
  return AppBar(
    title: Text(storage.accounts[storage.accountIndex]['name']),
  );
}
 // TODO choose month