import 'package:coin_client/loadinganimation.dart';
import 'package:coin_client/storage.dart';

import 'package:flutter/animation.dart';
import 'package:flutter/material.dart';

import 'common.dart';
import 'session.dart';
import 'networkutils.dart';

//TODO refactor
class LoadingScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final LoadingArgs args =
        ModalRoute.of(context).settings.arguments as LoadingArgs;

    return Scaffold(body: buildForm(Loader(args: args)));
  }
}

class Loader extends StatefulWidget {
  final LoadingArgs args;
  Loader({Key key, @required this.args}) : super(key: key);

  @override
  _LoaderState createState() {
    return _LoaderState();
  }
}

class _LoaderState extends State<Loader> with SingleTickerProviderStateMixin {
  Animation<double> animation;
  AnimationController controller;

  @override
  void initState() {
    super.initState();
    this.loadDataFromServer();
    this.controller =
        AnimationController(duration: const Duration(seconds: 1), vsync: this);
    this.animation =
        Tween<double>(begin: 10, end: 100).animate(this.controller);
    this.controller.forward();
    this.controller.repeat(reverse: true);
  }

  @override
  Widget build(BuildContext context) =>
      LoadingAnimation(animation: this.animation);

  @override
  void dispose() {
    this.controller.dispose();
    super.dispose();
  }

  Future<void> loadDataFromServer() async {
    switch (widget.args.type) {
      case LoadingType.REGISTER:
        this.loadDataFromServerOnRegister();
        break;
      case LoadingType.LOGIN:
        this.loadDataFromServerOnLogin();
        break;
      case LoadingType.CREATE_ACCOUNT:
        this.createAccount();
        break;
      case LoadingType.DELETE_ACCOUNT:
        this.deleteAccount();
        break;
      case LoadingType.EDIT_ACCOUNT:
        this.renameAccount();
        break;
      case LoadingType.GET_EVENTS:
        // TODO: Handle this case.
        break;
      case LoadingType.CREATE_EVENT:
        this.createEvent();
        break;
      case LoadingType.EDIT_EVENT:
        // TODO: Handle this case.
        // this.editEvent();
        break;
      case LoadingType.DELETE_EVENT:
        this.deleteEvent();
        break;
    }
  }

  Future<void> loadDataFromServerOnRegister() async {
    try {
      var response =
          await requestRegistration(widget.args.name, widget.args.password);
      processAuthorizationResponse(response);
      await _loadDataFromServerImpl();
    } catch (e) {
      displayError(this.context, e.toString());
      Navigator.of(this.context).pushReplacementNamed("/signup");
      return;
    }
    Navigator.of(this.context).pushReplacementNamed("/main");
  }

  Future<void> loadDataFromServerOnLogin() async {
    try {
      var response = await requestLogin(widget.args.name, widget.args.password);
      processAuthorizationResponse(response);
      await _loadDataFromServerImpl();
    } catch (e) {
      displayError(this.context, e.toString());
      Navigator.of(this.context).pushReplacementNamed("/login");
      return;
    }
    Navigator.of(this.context).pushReplacementNamed("/main");
  }

  Future<void> createAccount() async {
    try {
      var response = await requestCreateAccount(
        widget.args.name,
      );
      var responseBody = getResponseBody(response);
      var allAccountsResponse = await requestAccounts();
      processAccountsResponse(allAccountsResponse);
      setActiveAccountAfterCreate(responseBody);
    } catch (e) {
      displayError(this.context, e.toString());
      Navigator.of(this.context).pushReplacementNamed("/main");
      return;
    }
    Navigator.of(this.context).pushReplacementNamed("/main");
  }

  Future<void> renameAccount() async {
    try {
      var response =
          await requestRenameAccount(widget.args.id, widget.args.name);
      var responseBody = getResponseBody(response);
      var allAccountsResponse = await requestAccounts();
      processAccountsResponse(allAccountsResponse);
      setActiveAccountAfterRename(responseBody);
    } catch (e) {
      displayError(this.context, e.toString());
      Navigator.of(this.context).pushReplacementNamed("/main");
      return;
    }
    Navigator.of(this.context).pushReplacementNamed("/main");
  }

  Future<void> deleteAccount() async {
    try {
      var response = await requestDeleteAccount(
        widget.args.id,
      );
      var responseBody = getResponseBody(response);
      var allAccountsResponse = await requestAccounts();
      processAccountsResponse(allAccountsResponse);
      setActiveAccountAfterDelete(responseBody);
    } catch (e) {
      displayError(this.context, e.toString());
      Navigator.of(this.context).pushReplacementNamed("/main");
      return;
    }
    Navigator.of(this.context).pushReplacementNamed("/main");
  }

  Future<void> createEvent() async {
    try {
      var response = await requestCreateEvent(
        widget.args.dateTime,
        widget.args.diff,
        widget.args.description,
      );
      getResponseBody(response);
      response = await requestAllEvents();
      processEventsResponse(response);
    } catch (e) {
      displayError(this.context, e.toString());
      Navigator.of(this.context).pushReplacementNamed("/main");
      return;
    }
    Navigator.of(this.context).pushReplacementNamed("/main");
  }

  // Future<void> editEvent() async {
  //   try {
  //     var response = await requestEditEvent(widget.args.id, widget.args.name);
  //     getResponseBody(response);
  //     response = await requestAllEvents();
  //     processEventsResponse(response);
  //   } catch (e) {
  //     displayError(this.context, e.toString());
  //     Navigator.of(this.context).pushReplacementNamed("/main");
  //     return;
  //   }
  //   Navigator.of(this.context).pushReplacementNamed("/main");
  // }

  Future<void> deleteEvent() async {
    try {
      var response = await requestDeleteEvent(
        widget.args.id,
      );
      getResponseBody(response);
      response = await requestAllEvents();
      processEventsResponse(response);
    } catch (e) {
      displayError(this.context, e.toString());
      Navigator.of(this.context).pushReplacementNamed("/main");
      return;
    }
    Navigator.of(this.context).pushReplacementNamed("/main");
  }

  Future<void> _loadDataFromServerImpl() async {
    var accountsResponse = await requestAccounts();
    processAccountsResponse(accountsResponse);
    // int start_time = storage.currentMonthStart.millisecondsSinceEpoch ~/ 1000;
    // int end_time = DateTime(storage.currentMonthStart.year,
    //             storage.currentMonthStart.month - 1)
    //         .millisecondsSinceEpoch ~/
    //     1000;
    var eventsResponse = await requestAllEvents();
    // TODO load only significant events
    processEventsResponse(eventsResponse);
  }
}
