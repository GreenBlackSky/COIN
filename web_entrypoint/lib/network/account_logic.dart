import 'account_requests.dart';
import 'account_responses.dart';
import 'utils.dart';
import 'common.dart';

Future<void> syncAccounts() async {
  return requestAccounts().then(processAccountsResponse);
}

Future<void> createAccount(String name) async {
  var response = await requestCreateAccount(
    name,
  );
  var responseBody = getResponseBody(response);
  await requestAccounts().then(processAccountsResponse);
  setActiveAccountAfterCreate(responseBody);
  await syncData();
}

Future<void> renameAccount(int id, String name) async {
  var response = await requestRenameAccount(id, name);
  getResponseBody(response);
  await requestAccounts().then(processAccountsResponse);
}

Future<void> deleteAccount(int id) async {
  var response = await requestDeleteAccount(id);
  var responseBody = getResponseBody(response);
  await requestAccounts().then(processAccountsResponse);
  setActiveAccountAfterDelete(responseBody);
  await syncData();
}
