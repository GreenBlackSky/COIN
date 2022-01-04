import 'package:coin_client/storage.dart';
import 'package:flutter/material.dart';

import 'widgets/common/common.dart';
import 'widgets/accounts_list.dart';
import 'widgets/category_list.dart';
import 'widgets/burger_menu.dart';
import 'widgets/events_list.dart';
import 'widgets/events_graph.dart';
import 'widgets/drawer.dart';

final mainKey = new GlobalKey<_MainState>();

class MainScreen extends StatelessWidget {
  final MainWidget _mainWdget = new MainWidget(key: mainKey);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(storage.accounts[storage.accountIndex]['name']),
      ),
      body: buildForm(_mainWdget),
      drawer: buildDrawer(
          context, _mainWdget.cardNames, this.setCurrentWidgetIndex),
      floatingActionButton: FloatingActionButton(
        onPressed: addNewEventDialogMethod(context),
        child: Icon(Icons.add),
      ),
    );
  }

  void setCurrentWidgetIndex(int i) {
    mainKey.currentState.setCurrentWidgetIndex(i);
  }
}

class MainWidget extends StatefulWidget {
  MainWidget({Key key}) : super(key: key);
  // TODO choose month
  // TODO total, income and expence
  // TODO current balance
  final List<Widget> cardList = [
    EventGraph(),
    Text("month view"), //TODO month view
    EventsList(),
    Text("pie chart"), //TODO pie chart
    CategoryList(),
    Text("templates list"), //TODO templates list
    AccountList(),
    Text("settings"), //TODO settings
    Text("logout"), //TODO logout
  ];
  final List<String> cardNames = [
    "Graph view",
    "mMonth view",
    'List view',
    "Pie chart view",
    'Categories',
    "Templates",
    "Accounts",
    "Settings",
    "Logout",
  ];

  @override
  _MainState createState() => _MainState();
}

class _MainState extends State<MainWidget> {
  int currentWidgetIndex = 0;

  void setCurrentWidgetIndex(int i) {
    setState(() {
      this.currentWidgetIndex = i;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Center(child: widget.cardList[currentWidgetIndex]);
  }
}
