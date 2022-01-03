import 'package:flutter/material.dart';
import 'views/widgets/settings_screen.dart';
import 'views/login_view.dart';
import 'views/signup_view.dart';
import 'views/main_view.dart';
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
        '/main': (context) => MainScreen(),
        '/settings': (context) => SettingsScreen(),
        '/loading': (context) => LoadingScreen()
      },
    );
  }
}
