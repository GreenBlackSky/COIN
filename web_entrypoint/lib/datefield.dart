import 'package:flutter/material.dart';

import 'common.dart';

class DateField extends StatefulWidget {
  DateTime selectedDate = DateTime.now();
  @override
  _DateFieldState createState() {
    return _DateFieldState();
  }
}

class _DateFieldState extends State<DateField> {
  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: EdgeInsets.all(8.0),
        child: ElevatedButton(
            onPressed: () {
              _selectDate(context);
            },
            child: Text(
              dateToString(widget.selectedDate),
            )));
  }

  void _selectDate(BuildContext context) async {
    final DateTime selected = await showDatePicker(
      context: context,
      initialDate: widget.selectedDate,
      firstDate: DateTime(2010),
      lastDate: DateTime(2025),
    );
    if (selected != null && selected != widget.selectedDate)
      setState(() {
        widget.selectedDate = selected;
      });
  }
}
