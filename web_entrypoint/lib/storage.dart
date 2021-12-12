class DataStorage {
  DataStorage() {
    DateTime now = DateTime.now();
    this.currentMonthStart = DateTime(now.year, now.month).toUtc();
    this.currentMonthEnd = (now.month < 12)
        ? new DateTime(now.year, now.month + 1, 0)
        : new DateTime(now.year + 1, 1, 0);
  }
  String name;
  int account = -1;
  Map<int, String> accounts = {};
  // TODO categories
  int category = -1;
  DateTime currentMonthStart;
  DateTime currentMonthEnd;
  int monthStartBalance = 0;
  List events = []; // events in current month, event_time should be timestamp

  void clear() {
    this.name = "";
    this.account = -1;
    this.accounts.clear();
    this.category = -1;
    this.currentMonthStart =
        DateTime(DateTime.now().year, DateTime.now().month);
    this.events.clear();
  }
}

var storage = DataStorage();
