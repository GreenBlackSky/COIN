import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

import 'widgets/app_bar.dart';
import 'widgets/common/common.dart';
import 'widgets/drawer.dart';

import 'package:coin_client/storage.dart';

class PieChartView extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _PieChartViewState();
}

class _PieChartViewState extends State<PieChartView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(context),
      body: buildForm(PieChart()),
      drawer: buildDrawer(context),
    );
  }
}

class ChartData {
  ChartData(this.x, this.y, [this.color]);
  final String x;
  final double y;
  final Color color;
}

class PieChart extends StatefulWidget {
  const PieChart({Key key}) : super(key: key);

  @override
  State<PieChart> createState() => _PieChartState();
}

class _PieChartState extends State<PieChart> {
  @override
  Widget build(BuildContext context) {
    final List<ChartData> chartData = [];
    for (Map<String, dynamic> category in storage.categories) {
      chartData.add(ChartData(
          category['name'], storage.totals[category['id']], category['color']));
    }
    return SfCircularChart(
        legend: Legend(isVisible: true, position: LegendPosition.left),
        enableMultiSelection: true,
        series: <CircularSeries>[
          DoughnutSeries<ChartData, String>(
              dataSource: chartData,
              pointColorMapper: (ChartData data, _) => data.color,
              xValueMapper: (ChartData data, _) => data.x,
              yValueMapper: (ChartData data, _) => data.y,
              dataLabelSettings: DataLabelSettings(isVisible: true),
              selectionBehavior: SelectionBehavior(enable: true))
        ]);
  }
}
