import 'widgets/loading_animation.dart';

import 'package:flutter/material.dart';

import 'widgets/common/common.dart';
import '../network/network.dart';

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
    String endpoint = "/event_graph";
    String errorEndpoint = "/event_graph";
    try {
      switch (widget.args.type) {
        case LoadingType.REGISTER:
          errorEndpoint = "/signup";
          await loadDataFromServerOnRegister(
              widget.args.name, widget.args.password);
          break;
        case LoadingType.LOGIN:
          errorEndpoint = "/login";
          await loadDataFromServerOnLogin(
              widget.args.name, widget.args.password);
          break;
        case LoadingType.EDIT_USER:
          endpoint = widget.args.endpoint;
          errorEndpoint = "/settings";
          await editUser(
              widget.args.name, widget.args.password, widget.args.newPassword);
          break;
        case LoadingType.CREATE_ACCOUNT:
          await createAccount(widget.args.name);
          break;
        case LoadingType.EDIT_ACCOUNT:
          await renameAccount(widget.args.id, widget.args.name);
          break;
        case LoadingType.DELETE_ACCOUNT:
          await deleteAccount(widget.args.id);
          break;
        case LoadingType.CREATE_CATEGORY:
          await createCategory(widget.args.name, widget.args.color);
          break;
        case LoadingType.EDIT_CATEGORY:
          await editCategory(
              widget.args.id, widget.args.name, widget.args.color);
          break;
        case LoadingType.DELETE_CATEGORY:
          await deleteCategory(widget.args.id);
          break;
        case LoadingType.SYNC_DATA:
          await syncData();
          break;
        case LoadingType.CREATE_EVENT:
          await createEvent(
            widget.args.dateTime,
            widget.args.diff,
            widget.args.description,
            widget.args.id2,
          );
          break;
        case LoadingType.EDIT_EVENT:
          await editEvent(
            widget.args.id,
            widget.args.dateTime,
            widget.args.diff,
            widget.args.description,
            widget.args.id2,
          );
          break;
        case LoadingType.DELETE_EVENT:
          await deleteEvent(widget.args.id);
          break;
      }
    } catch (e) {
      displayError(this.context, e.toString());
      Navigator.of(this.context).pushReplacementNamed(errorEndpoint);
      return;
    }
    Navigator.of(this.context).pushReplacementNamed(endpoint);
  }
}
