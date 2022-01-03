import 'package:flutter/material.dart';

Widget buildListElementBase(String text, Function onEdit, Function onRemove,
    {Color color = Colors.blue}) {
  return Container(
    height: 50,
    color: color,
    child: Align(
        child:
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
      Padding(padding: EdgeInsets.all(8.0), child: Text(text)),
      Padding(
          padding: EdgeInsets.all(8.0),
          child: Row(children: [
            IconButton(
                icon: Icon(Icons.edit), color: Colors.black, onPressed: onEdit),
            IconButton(
              icon: Icon(Icons.delete),
              color: Colors.black,
              onPressed: onRemove,
            ),
          ]))
    ])),
    alignment: Alignment.centerRight,
  );
}
