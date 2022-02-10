import 'package:flutter/material.dart';

import 'widgets/topper.dart';
import 'widgets/common/element_list.dart';
import 'widgets/common/common.dart';
import 'widgets/drawer.dart';
import 'widgets/category_dialog.dart';

import 'package:coin_client/storage.dart';

class CategoryListView extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _CategoryListViewState();
}

class _CategoryListViewState extends State<CategoryListView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: Topper(context),
        body: buildForm(CategoryList(), 0.3),
        drawer: buildDrawer(context),
        floatingActionButton: FloatingActionButton(
            onPressed: addNewCategoryDialogMethod(context),
            child: Icon(Icons.add),
            tooltip: "Add new category"));
  }
}

class CategoryList extends ElementsList {
  final elements = storage.categories;

  @override
  Widget buildListElement(BuildContext context, var category) {
    Function onEdit = editCategoryDialogMethod(context, category);
    Function onRemove = deleteCategoryDialogMethod(context, category);
    return buildListElementBase(Text(category['name']), onEdit, onRemove,
        color: category['color']);
  }
}
