import 'package:flutter/material.dart';
import '../services/api_service.dart';

class SettingsScreen extends StatefulWidget {
  final ApiService api;
  const SettingsScreen({super.key, required this.api});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  Map<String, dynamic>? providers;
  Map<String, dynamic>? voice;
  Map<String, dynamic>? financials;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    final p = await widget.api.getProviderStatus();
    final v = await widget.api.getVoicePolicy();
    final f = await widget.api.getFinancials();
    setState(() { providers = p; voice = v; financials = f; });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings / Runtime')),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          Text('Provider mode: ${providers?['configured_mode'] ?? '-'}'),
          Text('Voice rule: ${voice?['rule'] ?? '-'}'),
          Text('Estimated value: ${financials?['total_estimated_value_usd'] ?? 0}'),
        ],
      ),
    );
  }
}
