import 'package:coin_client/common.dart';
import 'package:coin_client/storage.dart';
import 'package:flutter/material.dart';

//TODO edit/delete buttons
Widget buildEventsList() {
  return ListView.separated(
    padding: const EdgeInsets.all(8),
    itemCount: storage.events.length,
    itemBuilder: (BuildContext context, int index) {
      var event = storage.events[index];
      String date = dateToString(event['event_time']);
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
                ]),
            alignment: Alignment.centerRight),
      );
    },
    separatorBuilder: (BuildContext context, int index) => const Divider(),
  );
}
