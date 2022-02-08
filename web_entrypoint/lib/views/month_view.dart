import 'package:flutter/material.dart';

import 'widgets/app_bar.dart';
import 'widgets/event_dialog.dart';
import 'widgets/common/common.dart';
import 'widgets/drawer.dart';

class MonthView extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _MonthViewState();
}

class _MonthViewState extends State<MonthView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: buildAppBar(context),
        body: buildForm(Text("Month view"), 0.9),
        drawer: buildDrawer(context),
        floatingActionButton: FloatingActionButton(
            onPressed: addNewEventDialogMethod(context),
            child: Icon(Icons.add),
            tooltip: "Add new event"));
  }
}