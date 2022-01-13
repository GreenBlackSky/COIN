import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

import 'widgets/common/common.dart';
import 'widgets/drawer.dart';
import 'widgets/app_bar.dart';
import 'widgets/event_dialog.dart';

import 'package:coin_client/storage.dart';

class EventGraphView extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _EventGraphViewState();
}

class _EventGraphViewState extends State<EventGraphView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: buildAppBar(context),
        body: buildForm(EventGraph()),
        drawer: buildDrawer(context),
        floatingActionButton: FloatingActionButton(
            onPressed: addNewEventDialogMethod(context),
            child: Icon(Icons.add),
            tooltip: "Add new event"));
  }
}

class ChartData {
  ChartData({this.x, this.y});

  final DateTime x;
  final int y;
}

class EventGraph extends StatefulWidget {
  const EventGraph({Key key}) : super(key: key);

  @override
  State<EventGraph> createState() => _EventsGraphState();
}

class _EventsGraphState extends State<EventGraph> {
  @override
  Widget build(BuildContext context) {
    int balance = storage.monthStartBalance;
    List<ChartData> chartData = [];
    int eventIDX = 0;
    for (DateTime indexDay = storage.currentMonthStart;
        indexDay.month == storage.currentMonthStart.month;
        indexDay = indexDay.add(Duration(days: 1))) {
      int dayStartTimestamp = timestampFromDateTime(indexDay);
      int dayEndTimestamp =
          timestampFromDateTime(indexDay.add(Duration(days: 1)));
      while (eventIDX < storage.events.length &&
          storage.events[eventIDX]['event_time'] >= dayStartTimestamp &&
          storage.events[eventIDX]['event_time'] < dayEndTimestamp) {
        balance += storage.events[eventIDX]['diff'];
        eventIDX += 1;
      }
      chartData
          .add(ChartData(x: dateFromTimestamp(dayStartTimestamp), y: balance));
    }
    // TODO trackball
    // TODO link to event on trackball
    // TODO scale
    // TODO current total
    return SfCartesianChart(
        primaryXAxis: DateTimeAxis(
            intervalType: DateTimeIntervalType.days,
            minimum: storage.currentMonthStart,
            maximum: storage.currentMonthEnd),
        series: <ChartSeries<ChartData, DateTime>>[
          LineSeries<ChartData, DateTime>(
              dataSource: chartData,
              xValueMapper: (ChartData val, _) => val.x,
              yValueMapper: (ChartData val, _) => val.y)
        ]);
  }
}
