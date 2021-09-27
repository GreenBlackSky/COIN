import 'package:coin_client/common.dart';
import 'package:flutter/material.dart';

import 'accountslist.dart';
import 'burgermenu.dart';

class MainScreen extends StatelessWidget {
  final MainWidget _mainWdget = new MainWidget();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          leading: new Container(),
          title: AccountList(),
          actions: <Widget>[buildBurgerMenu(context)]),
      body: Center(
        child: buildForm(_mainWdget),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          //TODO Add event
        },
        child: Icon(Icons.add),
      ),
    );
  }
}

class MainWidget extends StatefulWidget {
  @override
  _MainState createState() => _MainState();
}

class _MainState extends State<MainWidget> {
  @override
  Widget build(BuildContext context) {
    var now = DateTime.now();
    var month = now.month;
    var daysInMonth = DateTime(now.year, now.month + 1, 0)
        .difference(DateTime(now.year, now.month, 0))
        .inDays;

    return ListView.separated(
      padding: const EdgeInsets.all(8),
      itemCount: daysInMonth,
      itemBuilder: (BuildContext context, int index) {
        return Container(
          height: 50,
          color: Colors.lightBlue,
          child: Align(
              child: Text('$month/$index'), alignment: Alignment.centerRight),
        );
      },
      separatorBuilder: (BuildContext context, int index) => const Divider(),
    );
  }
}
