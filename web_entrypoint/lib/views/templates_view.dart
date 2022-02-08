import 'package:flutter/material.dart';

import 'widgets/app_bar.dart';
import 'widgets/common/common.dart';
import 'widgets/drawer.dart';

class TemplatesView extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _TemplatesViewState();
}

class _TemplatesViewState extends State<TemplatesView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: buildAppBar(context),
        body: buildForm(Text("Templates"), 0.3),
        drawer: buildDrawer(context),
        floatingActionButton: FloatingActionButton(
            onPressed: () {},
            child: Icon(Icons.add),
            tooltip: "Add new template"));
  }
}
