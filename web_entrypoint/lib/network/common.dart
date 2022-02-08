import 'responses/user_responses.dart';
import 'requests/events_requests.dart';
import 'responses/events_responses.dart';
import 'requests/category_requests.dart';
import 'responses/category_responses.dart';

import 'package:coin_client/storage.dart';

Future<void> syncData() async {
  await requestEvents(storage.accounts[storage.accountIndex]['id'],
          storage.currentMonthStart, storage.currentMonthEnd)
      .then(processEventsResponse);
  await requestBalance(storage.accounts[storage.accountIndex]['id'],
          storage.currentMonthStart)
      .then(processMonthStartBalanceResponse);
  await requestCategories(storage.accounts[storage.accountIndex]['id'])
      .then(processCategories);
  await requestTotalsByCategory(storage.accounts[storage.accountIndex]['id'],
          storage.currentMonthStart, storage.currentMonthEnd)
      .then(processTotalsByCategory);
}
