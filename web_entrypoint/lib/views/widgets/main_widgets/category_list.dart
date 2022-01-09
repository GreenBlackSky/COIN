import 'package:flutter/material.dart';

import '../common/confirmation_dialog.dart';
import '../common/element_list.dart';
import '../common/common.dart';
import '../../../storage.dart';
import 'category_dialog.dart';

void Function() addNewCategoryDialogMethod(BuildContext context) {
  return baseCategoryDialog(context, "Add new category", "Create",
      LoadingType.CREATE_CATEGORY, -1, '', Colors.orange);
}

void Function() editCategoryDialogMethod(
    BuildContext context, Map<String, dynamic> category) {
  return baseCategoryDialog(
      context,
      "Edit category",
      "Edit",
      LoadingType.EDIT_CATEGORY,
      category['id'],
      category['name'],
      category['color']);
}

void Function() deleteCategoryDialogMethod(
    BuildContext context, Map<String, dynamic> category) {
  return confirmDialogMethod(
    context,
    "Are you sure you want to delete category?",
    "Delete category",
    () {
      Navigator.pushNamed(context, "/loading",
          arguments:
              LoadingArgs(LoadingType.DELETE_CATEGORY, id: category["id"]));
    },
  );
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
