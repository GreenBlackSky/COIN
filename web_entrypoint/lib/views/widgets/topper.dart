import 'package:flutter/material.dart';

import 'package:coin_client/storage.dart';
import 'common/common.dart';

void _setDateRange(BuildContext context, DateTimeRange range) {
  if (range == null) {
    return;
  }
  storage.periodStart = range.start;
  storage.periodEnd = range.end;
  Navigator.pushNamed(context, "/loading",
      arguments: LoadingArgs(LoadingType.SYNC_DATA));
}

String _buildPeriodStr() {
  String startYear = storage.periodStart.year.toString();
  String startMonth = storage.periodStart.month.toString().padLeft(2, '0');
  String startDay = storage.periodStart.day.toString().padLeft(2, '0');
  String endYear = storage.periodEnd.year.toString();
  String endMonth = storage.periodEnd.month.toString().padLeft(2, '0');
  String endDay = storage.periodEnd.day.toString().padLeft(2, '0');
  return "$startYear-$startMonth-$startDay - $endYear-$endMonth-$endDay";
}

class Topper extends AppBar {
  Topper(BuildContext context)
      : super(
            title: Row(children: [
          Text("COIN"),
          buildButton(storage.accounts[storage.accountIndex]['name'], () {
            Navigator.pushNamed(context, "/accounts_view");
          }),
          buildButton(_buildPeriodStr(), () {
            showDateRangePicker(
                context: context,
                firstDate: storage.periodStart,
                lastDate: storage.periodEnd,
                initialDateRange: DateTimeRange(
                  end: storage.periodEnd,
                  start: storage.periodStart,
                ),
                builder: (context, child) {
                  return FractionallySizedBox(
                    child: child,
                    widthFactor: 0.5,
                  );
                }).then((range) {
              _setDateRange(context, range);
            });
          })
        ])) {}
}
