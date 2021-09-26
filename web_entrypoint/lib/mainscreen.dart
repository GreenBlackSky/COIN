import 'package:coin_client/common.dart';
import 'package:flutter/material.dart';

import 'session.dart';
import 'storage.dart';

class MainScreen extends StatelessWidget {
  final MainWidget _mainWdget = new MainWidget();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          leading: new Container(),
          title: new DropdownButton<int>(
            value: storage.account,
            items: [
                  for (MapEntry e in storage.accounts.entries)
                    DropdownMenuItem<int>(child: Text(e.value), value: e.key)
                ] +
                [
                  DropdownMenuItem<int>(
                      child: Text("+ Add new account"), value: -1)
                ],
            onChanged: this.changeAccount,
          ),
          actions: <Widget>[buildPopUpMenu(context)]),
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

  void changeAccount(int accountID) {
    if (accountID == -1) {
      this.createAccount();
    } else {
      storage.account = accountID;
    }
  }

  void createAccount() {}

  Widget buildPopUpMenu(BuildContext context) {
    return PopupMenuButton<String>(
      onSelected: (String value) {
        switch (value) {
          case 'Logout':
            session.post('logout').catchError((_) {});
            session.clearSession();
            Navigator.of(context).pushNamed('/login');
            break;
          case 'Settings':
            Navigator.of(context).pushNamed('/settings');
            break;
        }
      },
      itemBuilder: (BuildContext context) {
        return [
          PopupMenuItem<String>(value: "Settings", child: Text("Settings")),
          PopupMenuItem<String>(value: "Logout", child: Text("Logout"))
        ];
      },
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
