import 'package:flutter/material.dart';
import 'package:carousel_slider/carousel_slider.dart';

import 'common.dart';
import 'accountslist.dart';
import 'burgermenu.dart';
import 'eventslist.dart';
import 'eventdialog.dart';

class MainScreen extends StatelessWidget {
  final MainWidget _mainWdget = new MainWidget();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          leading: new Container(),
          title: AccountList(),
          actions: <Widget>[buildBurgerMenu(context)]),
      body: buildForm(_mainWdget),
      floatingActionButton: FloatingActionButton(
        onPressed: addNewEventDialogMethod(context),
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
  int _currentIndex = 0;
  List<Widget> cardList = [
    Center(child: Text("graph")), //TODO graph
    Center(child: Text("pie chart")), //TODO pie chart
    Center(child: EventList()),
    Center(child: Text("month view")), //TODO month view
    Center(child: Text("templates list")), //TODO templates list
    Center(child: Text("categories list")), //TODO categories list
  ];

  List<T> map<T>(List list, Function handler) {
    List<T> result = [];
    for (var i = 0; i < list.length; i++) {
      result.add(handler(i, list[i]));
    }
    return result;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Expanded(
          child: CarouselSlider(
              options: CarouselOptions(
                onPageChanged: (index, reason) {
                  setState(() {
                    this._currentIndex = index;
                  });
                },
              ),
              items: this.cardList),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: map<Widget>(cardList, (index, url) {
            return Container(
              width: 10.0,
              height: 10.0,
              margin: EdgeInsets.symmetric(vertical: 10.0, horizontal: 2.0),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: this._currentIndex == index
                    ? Colors.blueAccent
                    : Colors.grey,
              ),
            );
          }),
        ),
      ],
    );
  }
}
