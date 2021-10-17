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
    List<ChartData> chartData = [
      ChartData(x: storage.currentMonthStart, y: storage.monthStartBalance)
    ];
    int balance = storage.monthStartBalance;
    for (Map<String, dynamic> event in storage.events) {
      balance += event['diff'];
      chartData.add(
          ChartData(x: dateFromTimestamp(event["event_time"]), y: balance));
    }
    chartData.add(ChartData(x: storage.currentMonthEnd, y: balance));
    //TODO crosshair
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
