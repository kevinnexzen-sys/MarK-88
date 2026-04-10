import 'package:flutter/material.dart';
import '../services/api_service.dart';

class PCControlScreen extends StatefulWidget {
  final ApiService api;
  const PCControlScreen({super.key, required this.api});

  @override
  State<PCControlScreen> createState() => _PCControlScreenState();
}

class _PCControlScreenState extends State<PCControlScreen> {
  List<dynamic> devices = [];

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    devices = await widget.api.getDevices();
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('PC Control')),
      body: ListView.builder(
        itemCount: devices.length,
        itemBuilder: (context, i) {
          final d = devices[i];
          return ListTile(
            title: Text(d['name'] ?? d['device_id'] ?? 'device'),
            subtitle: Text('Status: ${d['status']}'),
            trailing: IconButton(
              icon: const Icon(Icons.power_settings_new),
              onPressed: () async { await widget.api.wakeDevice(d['id']); },
            ),
          );
        },
      ),
    );
  }
}
