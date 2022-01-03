import 'package:flutter/material.dart';
import 'ui/settingsscreen.dart';
import 'ui/login.dart';
import 'ui/signup.dart';
import 'ui/mainscreen.dart';
import 'ui/loadingscreen.dart';

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
