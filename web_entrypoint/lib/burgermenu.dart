import 'package:coin_client/storage.dart';
import 'package:flutter/material.dart';

import 'session.dart';

Widget buildBurgerMenu(BuildContext context) {
  return PopupMenuButton<String>(
    onSelected: (String value) {
      switch (value) {
        case 'Logout':
          session.post('logout').catchError((_) {});
          session.clearSession();
          storage.clear();
          Navigator.of(context).pushNamed('/login');
          break;
        case 'Settings':
          Navigator.of(context).pushNamed('/settings');
          break;
      }
    },
    itemBuilder: (BuildContext context) {
      return [
        PopupMenuItem<String>(value: "Settings", child: Text("Settings")),
        PopupMenuItem<String>(value: "Logout", child: Text("Logout"))
      ];
    },
  );
}
