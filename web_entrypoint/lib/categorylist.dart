import 'package:flutter/material.dart';

import 'common.dart';
import 'storage.dart';
import 'categorydialog.dart';
import 'confirmationdialog.dart';

class CategoryList extends StatefulWidget {
  const CategoryList({Key key}) : super(key: key);

  @override
  State<CategoryList> createState() => _CategoryListState();
}

class _CategoryListState extends State<CategoryList> {
  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(8),
      itemCount: storage.categories.length,
      itemBuilder: (BuildContext context, int index) {
        var category = storage.categories[index];
        return Container(
          height: 50,
          color: Colors.lightBlue, // TODO category color
          child: Align(
              child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(category['name'].toString())),
                    Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Row(children: [
                          IconButton(
                              icon: Icon(Icons.edit),
                              color: Colors.black,
                              onPressed:
                                  editCategoryDialogMethod(context, category)),
                          IconButton(
                            icon: Icon(Icons.delete),
                            color: Colors.black,
                            onPressed: confirmDialogMethod(
                              context,
                              "Are you sure you want to delete event?",
                              "Delete event",
                              () {
                                Navigator.pushNamed(context, "/loading",
                                    arguments: LoadingArgs(
                                        LoadingType.DELETE_CATEGORY,
                                        id: category["id"]));
                              },
                            ),
                          )
                        ])),
                  ]),
              alignment: Alignment.centerRight),
        );
      },
      separatorBuilder: (BuildContext context, int index) => const Divider(),
    );
  }
}
