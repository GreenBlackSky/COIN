import 'package:flutter/material.dart';
import 'package:carousel_slider/carousel_slider.dart';

import 'common.dart';
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
  int _currentIndex = 0;
  List<Widget> cardList = [
    Center(child: Text("1")), // graph
    Center(child: Text("2")), // pie chart
    Center(child: Text("3")), // month
    Center(child: Text("4")), // comming events
    Center(child: Text("5")), // templates
    Center(child: Text("6")), // categories
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
        CarouselSlider(
            options: CarouselOptions(
              onPageChanged: (index, reason) {
                setState(() {
                  this._currentIndex = index;
                });
              },
            ),
            items: this.cardList),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: map<Widget>(cardList, (index, url) {
            return Container(
              width: 10.0,
              height: 10.0,
              margin: EdgeInsets.symmetric(vertical: 10.0, horizontal: 2.0),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _currentIndex == index ? Colors.blueAccent : Colors.grey,
              ),
            );
          }),
        ),
      ],
    );
  }
}
