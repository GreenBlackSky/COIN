import 'package:coin_client/common.dart';
import 'package:coin_client/storage.dart';
import 'package:flutter/material.dart';

class EventList extends StatefulWidget {
  const EventList({Key key}) : super(key: key);

  @override
  State<EventList> createState() => _EventListState();
}

class _EventListState extends State<EventList> {
  // Null Function() editEventMethod(Map<String, dynamic> event) {
  //   return () {
  //     Navigator.pushNamed(context, "/loading",
  //         arguments: LoadingArgs(LoadingType.EDIT_EVENT, id: event["id"]));
  //   };
  // }

  Null Function() deleteEventMethod(Map<String, dynamic> event) {
    //TODO confirmation
    return () {
      Navigator.pushNamed(context, "/loading",
          arguments: LoadingArgs(LoadingType.DELETE_EVENT, id: event["id"]));
    };
  }

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(8),
      itemCount: storage.events.length,
      itemBuilder: (BuildContext context, int index) {
        var event = storage.events[index];
        String date = timestampToString(event['event_time']);
        return Container(
          height: 50,
          color: Colors.lightBlue,
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
                              // onPressed: this.editEventMethod(event)),
                              onPressed: () {}),
                          IconButton(
                            icon: Icon(Icons.delete),
                            color: Colors.black,
                            onPressed: this.deleteEventMethod(event),
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
