class BackgroundMonitor {
  Map<String, dynamic> snapshot(String activeScreen) {
    return {"activeScreen": activeScreen, "eventType": "mobile_interaction"};
  }
}
