import 'package:coin_client/storage.dart';
import 'package:flutter/material.dart';

import 'widgets/common/common.dart';
import 'widgets/main_widgets/account_list.dart';
import 'widgets/main_widgets/category_list.dart';
import 'widgets/burger_menu.dart';
import 'widgets/main_widgets/event_list.dart';
import 'widgets/main_widgets/event_graph.dart';
import 'widgets/drawer.dart';
import 'widgets/add_button.dart';

class _MainWidgetInfo {
  String name;
  Widget widget;
  String tooltip;
  void Function() Function(BuildContext) addNewStuff;
  bool addButtonVisible;

  _MainWidgetInfo(String name, Widget widget,
      [String tooltip, void Function(BuildContext) addNewStuff]) {
    this.name = name;
    this.widget = widget;
    this.tooltip = tooltip;
    this.addNewStuff = addNewStuff;
    this.addButtonVisible = (tooltip != null);
  }
}

class MainScreen extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _MainSceenState();
}

class _MainSceenState extends State<MainScreen> {
  int currentWidgetIndex = 0;

  final List<_MainWidgetInfo> widgets = [
    _MainWidgetInfo(
        "Graph view", EventGraph(), "Add new event", addNewEventDialogMethod),
    _MainWidgetInfo(
        "List view", EventsList(), "Add new event", addNewEventDialogMethod),
    _MainWidgetInfo("Month view", Text("month view"), "Add new event",
        addNewEventDialogMethod),
    _MainWidgetInfo("Pie chart", Text("pie chart")),
    _MainWidgetInfo("Categories", CategoryList(), "Add new category",
        addNewCategoryDialogMethod),
    _MainWidgetInfo("Templates", Text("templates list"), "Add new template",
        (BuildContext c) {}),
    _MainWidgetInfo("Accounts", AccountList(), "Add new account",
        addNewAccountDialogMethod),
    _MainWidgetInfo("Settings", Text("settings")),
    _MainWidgetInfo("Logout", Text("logout")),
  ];

  // TODO choose month
  // TODO total, income and expence
  // TODO current balance

  @override
  Widget build(BuildContext context) {
    _MainWidgetInfo currentWidget = this.widgets[this.currentWidgetIndex];
    return Scaffold(
        appBar: AppBar(
          title: Text(storage.accounts[storage.accountIndex]['name']),
        ),
        body: buildForm(currentWidget.widget),
        drawer: buildDrawer(context, this.widgets.map((w) => w.name).toList(),
            this.setCurrentWidgetIndex),
        floatingActionButton: AddButton(currentWidget.addButtonVisible,
            currentWidget.tooltip, currentWidget.addNewStuff));
  }

  void setCurrentWidgetIndex(int i) {
    this.setState(() {
      this.currentWidgetIndex = i;
    });
  }
}
