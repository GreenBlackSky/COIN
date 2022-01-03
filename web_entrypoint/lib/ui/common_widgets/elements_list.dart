import 'package:flutter/material.dart';

class ElementsList extends StatefulWidget {
  ElementsList({Key key}) : super(key: key);
  List elements;

  @override
  State<ElementsList> createState() => _ElementsListState();

  Widget buildListElement(BuildContext context, var element) {}
}

class _ElementsListState extends State<ElementsList> {
  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(8),
      itemCount: this.widget.elements.length,
      itemBuilder: (BuildContext context, int index) {
        return this
            .widget
            .buildListElement(context, this.widget.elements[index]);
      },
      separatorBuilder: (BuildContext context, int index) => const Divider(),
    );
  }
}
