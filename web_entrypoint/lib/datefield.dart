import 'package:flutter/material.dart';

class DateField extends StatefulWidget {
  @override
  _DateFieldState createState() {
    return _DateFieldState();
  }
}

class _DateFieldState extends State<DateField> {
  DateTime selectedDate = DateTime.now();
  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: EdgeInsets.all(8.0),
        child: ElevatedButton(
          onPressed: () {
            _selectDate(context);
          },
          child: Text(
              "${this.selectedDate.day}/${this.selectedDate.month}/${this.selectedDate.year}"),
        ));
  }

  void _selectDate(BuildContext context) async {
    final DateTime selected = await showDatePicker(
      context: context,
      initialDate: this.selectedDate,
      firstDate: DateTime(2010),
      lastDate: DateTime(2025),
    );
    if (selected != null && selected != this.selectedDate)
      setState(() {
        this.selectedDate = selected;
      });
  }
}
