class DataStorage {
  String name;
  int account = -1;
  DateTime currentMonthStart =
      DateTime(DateTime.now().year, DateTime.now().month).toUtc();
  Map<int, String> accounts = {};
  List events = [];

  void clear() {
    this.name = "";
    this.account = -1;
    this.accounts.clear();
    this.currentMonthStart =
        DateTime(DateTime.now().year, DateTime.now().month).toUtc();
    this.events.clear();
  }
}

var storage = DataStorage();
