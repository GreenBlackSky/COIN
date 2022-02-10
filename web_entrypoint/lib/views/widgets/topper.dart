import 'dart:developer';

import 'package:flutter/material.dart';

import 'package:coin_client/storage.dart';
import 'common/common.dart';

class Topper extends AppBar {
  Topper(BuildContext context)
      : super(
            title: Row(children: [
          Text("COIN"),
          buildButton(storage.accounts[storage.accountIndex]['name'], () {
            Navigator.pushNamed(context, "/accounts_view");
          }),
          buildButton("${storage.periodStart} - ${storage.periodEnd}", () {
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
                });
          })
        ])) {}
}
