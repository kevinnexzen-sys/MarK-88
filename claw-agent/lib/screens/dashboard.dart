import 'package:flutter/material.dart';
import '../services/api_service.dart';

class DashboardScreen extends StatefulWidget {
  final ApiService api;
  const DashboardScreen({super.key, required this.api});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  Map<String, dynamic>? summary;
  Map<String, dynamic>? providers;
  Map<String, dynamic>? voice;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    widget.api.mobileEvent('screen_view', 'dashboard');
    load();
  }

  Future<void> load() async {
    final s = await widget.api.getSummary();
    final p = await widget.api.getProviderStatus();
    final v = await widget.api.getVoicePolicy();
    setState(() {
      summary = s;
      providers = p;
      voice = v;
      loading = false;
    });
  }

  Widget card(String title, String value) => Card(child: Padding(
    padding: const EdgeInsets.all(12), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(title, style: const TextStyle(fontWeight: FontWeight.bold)), const SizedBox(height: 6), Text(value)]),
  ));

  @override
  Widget build(BuildContext context) {
    if (loading) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    return Scaffold(
      appBar: AppBar(title: const Text('MARK / CLAW Dashboard')),
      body: RefreshIndicator(
        onRefresh: load,
        child: ListView(
          padding: const EdgeInsets.all(12),
          children: [
            card('CEO Heartbeat', '${summary?['health']?['heartbeat'] ?? '-'}'),
            card('Workers Online', '${summary?['health']?['workers_online'] ?? 0}'),
            card('Devices Online', '${summary?['health']?['devices_online'] ?? 0}'),
            card('Pending Approvals', '${summary?['health']?['pending_approvals'] ?? 0}'),
            card('Provider Mode', '${providers?['configured_mode'] ?? '-'}'),
            card('Voice Rule', '${voice?['rule'] ?? '-'}'),
            card('Mobile Speaks', '${voice?['mobile_speaks'] ?? false} | Desktop Speaks: ${voice?['desktop_speaks'] ?? false}'),
          ],
        ),
      ),
    );
  }
}
