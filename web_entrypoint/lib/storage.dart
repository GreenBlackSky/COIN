class DataStorage {
  DataStorage() {
    DateTime now = DateTime.now();
    this.currentMonthStart = DateTime(now.year, now.month).toUtc();
    this.currentMonthEnd = (now.month < 12)
        ? new DateTime(now.year, now.month + 1, 0)
        : new DateTime(now.year + 1, 1, 0);
  }
  String name;
  int accountIndex = -1;
  List accounts = [];
  int category = -1;
  List categories = [];
  Map totals = {};
  List events = []; // events in current month, event_time should be timestamp
  DateTime currentMonthStart;
  DateTime currentMonthEnd;
  int monthStartBalance = 0;

  void clear() {
    this.name = "";
    this.accountIndex = -1;
    this.accounts.clear();
    this.category = -1;
    this.categories.clear();
    this.totals.clear();
    DateTime now = DateTime.now().toUtc();
    this.currentMonthStart = DateTime(now.year, now.month);
    this.currentMonthEnd = (now.month < 12)
        ? new DateTime(now.year, now.month + 1, 0)
        : new DateTime(now.year + 1, 1, 0);
    this.events.clear();
  }
}

var storage = DataStorage();
