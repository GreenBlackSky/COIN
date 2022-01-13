import 'package:flutter/material.dart';

import 'package:coin_client/network/session.dart';
import 'package:coin_client/storage.dart';

import 'common/confirmation_dialog.dart';

Map<String, String> views = {
  "Graph view": "/event_graph",
  "List view": "/event_list",
  "Month view": "/month_view",
  "Pie chart": "/pie_chart_view",
  "Categories": "/category_view",
  "Templates": "/templates_view",
  "Accounts": "/accounts_view",
  "Settings": "/settings",
  // "Logout": "/event_graph",
};

Widget buildDrawer(BuildContext context) {
  List<Widget> tiles = [];
  for (MapEntry<String, String> e in views.entries) {
    Widget tile = ListTile(
      title: Text(e.key),
      onTap: () {
        Navigator.pushNamed(context, e.value);
      },
    );
    tiles.add(tile);
  }
  tiles.add(ListTile(
      title: Text("Logout"),
      onTap: confirmDialogMethod(context, "Are you sure, you want to log out?",
          "Log out", logoutMethod(context))));
  return Drawer(
    child: ListView(
      padding: EdgeInsets.zero,
      children: tiles,
    ),
  );
}

void Function() logoutMethod(BuildContext context) {
  return () {
    session.post('logout').catchError((_) {});
    session.clearSession();
    storage.clear();
    Navigator.of(context).pushNamed('/login');
  };
}
