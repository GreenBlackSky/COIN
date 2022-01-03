import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

import 'common.dart';
import 'storage.dart';

class ChartData {
  ChartData({this.x, this.y});

  final DateTime x;
  final int y;
}

class GraphView extends StatefulWidget {
  const GraphView({Key key}) : super(key: key);

  @override
  State<GraphView> createState() => _GraphViewState();
}

class _GraphViewState extends State<GraphView> {
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
    // TODO total
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
