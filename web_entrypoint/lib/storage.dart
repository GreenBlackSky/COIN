class DataStorage {
  String name;
  int account = -1;
  Map<int, String> accounts = {-1: "ERROR!!"};
  List<int> events = [];
}

var storage = DataStorage();
