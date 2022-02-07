import 'package:flutter/material.dart';

import 'category_requests.dart';
import 'category_responses.dart';
import 'common.dart';

import 'package:coin_client/storage.dart';

Future<void> createCategory(String name, Color color) async {
  await requestCreateCategory(
          name, color, storage.accounts[storage.accountIndex]['id'])
      .then(processAddCategoryResponse);
}

Future<void> editCategory(int categoryID, String name, Color color) async {
  await requestEditCategory(
          categoryID, name, color, storage.accounts[storage.accountIndex]['id'])
      .then(processEditCategoryResponse);
}

Future<void> deleteCategory(int categoryID) async {
  await requestDeleteCategory(
          categoryID, storage.accounts[storage.accountIndex]['id'])
      .then(processRemoveCategoryResponse);
  syncData();
}
