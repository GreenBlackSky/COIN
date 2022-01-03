import 'package:flutter/material.dart';

Future<String> Function() confirmDialogMethod(BuildContext context,
    String title, String buttonText, void Function() onPressed) {
  return () {
    return showDialog<String>(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text(title),
            actions: <Widget>[
              TextButton(
                child: Text(buttonText),
                onPressed: onPressed,
              ),
              TextButton(
                child: const Text('Cancel'),
                onPressed: () {
                  Navigator.pop(context, 'Cancel');
                },
              ),
            ],
          );
        });
  };
}
