import 'package:flutter/material.dart';

import 'widgets/app_bar.dart';
import 'widgets/event_dialog.dart';
import 'widgets/common/element_list.dart';
import 'widgets/common/common.dart';
import 'widgets/drawer.dart';

import '../storage.dart';

class EventListView extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _EventListViewState();
}

class _EventListViewState extends State<EventListView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: buildAppBar(context),
        body: buildForm(EventsList()),
        drawer: buildDrawer(context),
        floatingActionButton: FloatingActionButton(
            onPressed: addNewEventDialogMethod(context),
            child: Icon(Icons.add),
            tooltip: "Add new event"));
  }
}

class EventsList extends ElementsList {
  final elements = storage.events;

  @override
  Widget buildListElement(BuildContext context, var event) {
    String date = timestampToString(event['event_time']);
    String diff = event['diff'].toString();
    Widget description =
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
      Padding(padding: EdgeInsets.all(8.0), child: Text(date)),
      Padding(padding: EdgeInsets.all(8.0), child: Text(diff)),
      Padding(padding: EdgeInsets.all(8.0), child: Text(event['description'])),
    ]);
    Function onEdit = editEventDialogMethod(context, event);
    Function onRemove = deleteEventDialogMethod(context, event);
    var category = storage.categories.where((element) {
      return element['id'] == event['category_id'];
    }).first;
    Color color = category['color'];
    return buildListElementBase(description, onEdit, onRemove, color: color);
  }
}
