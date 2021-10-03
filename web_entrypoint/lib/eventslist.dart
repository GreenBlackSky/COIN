import 'package:flutter/material.dart';

//TODO show events
Widget buildEventsList() {
  return ListView.separated(
    padding: const EdgeInsets.all(8),
    itemCount: 10,
    itemBuilder: (BuildContext context, int index) {
      return Container(
        height: 50,
        color: Colors.lightBlue,
        child: Align(child: Text("A"), alignment: Alignment.centerRight),
      );
    },
    separatorBuilder: (BuildContext context, int index) => const Divider(),
  );
}
