import 'package:flutter/material.dart';

Map<String, String> views = {
  "Graph view": "/event_graph",
  "List view": "/event_list",
  "Month view": "/month_view",
  "Pie chart": "/pie_chart_view",
  "Categories": "/category_view",
  "Templates": "/templates_view",
  "Accounts": "/accounts_view",
  "Settings": "/settings",
  "Logout": "/event_graph",
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
  return Drawer(
    child: ListView(
      padding: EdgeInsets.zero,
      children: tiles,
    ),
  );
}
