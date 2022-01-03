import 'package:coin_client/ui/common_widgets/common.dart';
import 'package:coin_client/storage.dart';
import 'package:flutter/material.dart';

import 'widgets/eventdialog.dart';
import 'common_widgets/confirmation_dialog.dart';

class EventList extends StatefulWidget {
  const EventList({Key key}) : super(key: key);

  @override
  State<EventList> createState() => _EventListState();
}

class _EventListState extends State<EventList> {
  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      //TODO show only comming events
      padding: const EdgeInsets.all(8),
      itemCount: storage.events.length,
      itemBuilder: (BuildContext context, int index) {
        var event = storage.events[index];
        String date = timestampToString(event['event_time']);
        var category = storage.categories.where((element) {
          return element['id'] == event['category_id'];
        }).first;
        return Container(
          height: 50,
          color: category['color'],
          child: Align(
              child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(event['diff'].toString())),
                    Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(event['description'])),
                    Padding(padding: EdgeInsets.all(8.0), child: Text(date)),
                    Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Row(children: [
                          IconButton(
                              icon: Icon(Icons.edit),
                              color: Colors.black,
                              onPressed: editEventDialogMethod(context, event)),
                          IconButton(
                            icon: Icon(Icons.delete),
                            color: Colors.black,
                            onPressed: confirmDialogMethod(
                              context,
                              "Are you sure you want to delete event?",
                              "Delete event",
                              () {
                                Navigator.pushNamed(context, "/loading",
                                    arguments: LoadingArgs(
                                        LoadingType.DELETE_EVENT,
                                        id: event["id"]));
                              },
                            ),
                          )
                        ])),
                  ]),
              alignment: Alignment.centerRight),
        );
      },
      separatorBuilder: (BuildContext context, int index) => const Divider(),
    );
  }
}
