import 'requests.dart';
import 'response_processor.dart';
import 'events_requests.dart';
import 'events_responses.dart';
import 'category_requests.dart';
import 'category_responses.dart';

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
