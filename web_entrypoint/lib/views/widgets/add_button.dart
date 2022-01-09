import 'package:flutter/material.dart';

class AddButton extends StatefulWidget {
  bool isVisible;
  String tooltip;
  void Function() Function(BuildContext) addStuff;

  AddButton(bool isVisible,
      [String tooltip, void Function(BuildContext) addStuff]) {
    this.isVisible = isVisible;
    if (this.isVisible) {
      this.tooltip = tooltip;
      this.addStuff = addStuff;
    } else {
      this.tooltip = "";
      this.addStuff = (BuildContext b) {};
    }
  }

  @override
  State<StatefulWidget> createState() => _AddButtonState();
}

class _AddButtonState extends State<AddButton> {
  @override
  Widget build(BuildContext context) {
    return Visibility(
      visible: this.widget.isVisible,
      child: FloatingActionButton(
        onPressed: this.widget.addStuff(context),
        child: Row(children: [Icon(Icons.add), Icon(Icons.add_reaction)]),
        tooltip: this.widget.tooltip,
      ),
    );
  }
}
