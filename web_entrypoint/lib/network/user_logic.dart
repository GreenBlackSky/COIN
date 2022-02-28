import 'requests/user_requests.dart';
import 'responses/user_responses.dart';
import 'account_logic.dart';
import 'common.dart';

Future<void> loadDataFromServerOnRegister(String name, String password) async {
  await requestRegistration(name, password).then(processAuthorizationResponse);
  await syncAccounts();
  await syncData();
}

Future<void> loadDataFromServerOnLogin(String name, String password) async {
  await requestLogin(name, password).then(processAuthorizationResponse);
  await syncAccounts();
  await syncData();
}

Future<void> editUser(String name, String password, String newPassword) async {
  await requestEditUser(name, password, newPassword);
  await syncUser();
}
