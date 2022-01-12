import 'package:flutter/material.dart';

import 'views/login_view.dart';
import 'views/signup_view.dart';
import 'views/event_graph.dart';
import 'views/event_list.dart';
import 'views/month_view.dart';
import 'views/pie_chart_view.dart';
import 'views/category_list.dart';
import 'views/templates_view.dart';
import 'views/account_list.dart';
import 'views/settings_view.dart';
import 'views/loading_view.dart';

void main() => runApp(App());

// TODO check authorization on routes
class App extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "COIN",
      initialRoute: '/login',
      routes: {
        '/login': (context) => LogInScreen(),
        '/signup': (context) => SignUpScreen(),
        '/event_graph': (context) => EventGraphView(),
        '/event_list': (context) => EventListView(),
        '/month_view': (context) => MonthView(),
        '/pie_chart_view': (context) => PieChartView(),
        '/category_view': (context) => CategoryListView(),
        '/templates_view': (context) => TemplatesView(),
        '/accounts_view': (context) => AccountListView(),
        '/settings': (context) => SettingsScreen(),
        '/loading': (context) => LoadingScreen()
      },
    );
  }
}
