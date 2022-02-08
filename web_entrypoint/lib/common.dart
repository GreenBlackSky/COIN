DateTime dateFromTimestamp(int timestamp) {
  return DateTime.fromMillisecondsSinceEpoch(timestamp * 1000);
}

int timestampFromDateTime(DateTime dateTime) {
  return dateTime.millisecondsSinceEpoch ~/ 1000;
}

String dateToString(DateTime date) {
  return "${date.day}/${date.month}/${date.year}";
}

String timestampToString(int timestamp) {
  var date = dateFromTimestamp(timestamp);
  return "${date.day}/${date.month}/${date.year}";
}
