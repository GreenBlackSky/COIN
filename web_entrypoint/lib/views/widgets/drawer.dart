import 'package:flutter/material.dart';

Widget buildDrawer(
    BuildContext context, List<String> names, Function(int) setIndex) {
  List<Widget> tiles = [];
  for (int i = 0; i < names.length; i++) {
    String name = names[i];
    Widget tile = ListTile(
      title: Text(name),
      onTap: () {
        setIndex(i);
        Navigator.pop(context);
      },
    );
    tiles.add(tile);
  }
  return Drawer(
    child: ListView(
      // Important: Remove any padding from the ListView.
      padding: EdgeInsets.zero,
      children: tiles,
    ),
  );
}
