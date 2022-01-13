import 'package:flutter/material.dart';

import 'widgets/app_bar.dart';
import 'widgets/common/common.dart';
import 'widgets/drawer.dart';

class PieChartView extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _PieChartViewState();
}

class _PieChartViewState extends State<PieChartView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(context),
      body: buildForm(Text("Pie chart")),
      drawer: buildDrawer(context),
    );
  }
}
