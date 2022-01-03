import 'package:flutter/material.dart';

import 'dialogues/event_dialog.dart';
import 'common/confirmation_dialog.dart';
import 'common/elements_list.dart';
import 'common/common.dart';
import '../../storage.dart';

void Function() addNewEventDialogMethod(BuildContext context) {
  return baseEventDialog(
      context,
      "Add new event",
      "Create",
      LoadingType.CREATE_EVENT,
      -1,
      0,
      DateTime.now(),
      storage.account,
      "",
      storage.categories[0]['id']);
}

void Function() editEventDialogMethod(
    BuildContext context, Map<String, dynamic> event) {
  return baseEventDialog(
      context,
      "Edit event",
      "Edit",
      LoadingType.EDIT_EVENT,
      event['id'],
      event["diff"],
      dateFromTimestamp(event["event_time"]),
      event['account_id'],
      event["description"],
      event['category_id']);
}

Function deleteEventDialogMethod(
    BuildContext context, Map<String, dynamic> event) {
  return confirmDialogMethod(
    context,
    "Are you sure you want to delete event?",
    "Delete event",
    () {
      Navigator.pushNamed(context, "/loading",
          arguments: LoadingArgs(LoadingType.DELETE_EVENT,
              id: event["id"], id2: event['account_id']));
    },
  );
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
