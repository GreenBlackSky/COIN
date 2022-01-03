import 'package:flutter/material.dart';

import 'requests.dart';
import 'responseprocessor.dart';

import 'storage.dart';

Future<void> loadDataFromServerOnRegister(String name, String password) async {
  await requestRegistration(name, password).then(processAuthorizationResponse);
  await requestAccounts().then(processAccountsResponse);
  await requestCategories().then(processCategories);
  await syncData();
}

Future<void> loadDataFromServerOnLogin(String name, String password) async {
  await requestLogin(name, password).then(processAuthorizationResponse);
  await requestAccounts().then(processAccountsResponse);
  await requestCategories().then(processCategories);
  await syncData();
}

Future<void> editUser(String name, String password, String newPassword) async {
  await requestEditUser(name, password, newPassword);
}

Future<void> createAccount(String name) async {
  var response = await requestCreateAccount(
    name,
  );
  var responseBody = getResponseBody(response);
  await requestAccounts().then(processAccountsResponse);
  await requestCategories().then(processCategories);
  setActiveAccountAfterCreate(responseBody);
  await syncData();
}

Future<void> renameAccount(int id, String name) async {
  var response = await requestRenameAccount(id, name);
  var responseBody = getResponseBody(response);
  await requestAccounts().then(processAccountsResponse);
  setActiveAccountAfterRename(responseBody);
}

Future<void> deleteAccount(int id) async {
  var response = await requestDeleteAccount(id);
  var responseBody = getResponseBody(response);
  await requestAccounts().then(processAccountsResponse);
  await requestCategories().then(processCategories);
  setActiveAccountAfterDelete(responseBody);
  await syncData();
}

Future<void> createCategory(String name, Color color) async {
  await requestCreateCategory(name, color).then(processCategories);
}

Future<void> editCategory(int categoryID, String name, Color color) async {
  await requestEditCategory(categoryID, name, color)
      .then(processEditCategoryResponse);
}

Future<void> deleteCategory(int categoryID) async {
  await requestDeleteCategory(categoryID).then(processRemoveCategoryResponse);
  syncData();
}

Future<void> syncData() async {
  await requestEvents(
          storage.account, storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
  await requestBalance(storage.account, storage.currentMonthStart)
      .then(processMonthStartBalanceResponse);
}

Future<void> createEvent(DateTime dateTime, int diff, String description,
    int categoryID, int accountID) async {
  var response = await requestCreateEvent(
      accountID, dateTime, diff, description, categoryID);
  getResponseBody(response);
  await syncData();
}

Future<void> editEvent(int id, DateTime dateTime, int diff, String description,
    int categoryID, int accountID) async {
  var response = await requestEditEvent(
      id, accountID, dateTime, diff, description, categoryID);
  getResponseBody(response);
  await syncData();
}

Future<void> deleteEvent(int id) async {
  var response = await requestDeleteEvent(id);
  getResponseBody(response);
  await syncData();
}
