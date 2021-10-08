import 'package:coin_client/settingsscreen.dart';
import 'package:flutter/material.dart';
import 'login.dart';
import 'signup.dart';
import 'mainscreen.dart';
import 'loadingscreen.dart';

void main() => runApp(App());

//TODO theme
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
