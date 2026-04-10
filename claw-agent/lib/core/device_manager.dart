class DeviceManager {
  Map<String, dynamic> wakeCommand(String deviceId, String mac) {
    return {"device_id": deviceId, "mac": mac, "type": "wake_pc"};
  }
}
