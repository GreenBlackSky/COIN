class DataStorage {
  String name;
  int account = -1;
  Map<int, String> accounts = {};
  List<int> events = [];

  void clear() {
    this.name = "";
    this.account = -1;
    this.accounts.clear();
    this.events.clear();
  }
}

var storage = DataStorage();
