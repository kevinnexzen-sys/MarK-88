import 'package:flutter/material.dart';
import '../services/api_service.dart';

class KnowledgeScreen extends StatefulWidget {
  final ApiService api;
  const KnowledgeScreen({super.key, required this.api});

  @override
  State<KnowledgeScreen> createState() => _KnowledgeScreenState();
}

class _KnowledgeScreenState extends State<KnowledgeScreen> {
  Map<String, dynamic>? knowledge;
  Map<String, dynamic>? skills;
  Map<String, dynamic>? automations;
  Map<String, dynamic>? patterns;

  @override
  void initState() {
    super.initState();
    widget.api.mobileEvent('screen_view', 'knowledge_screen');
    load();
  }

  Future<void> load() async {
    final k = await widget.api.getKnowledge();
    final s = await widget.api.getSkills();
    final a = await widget.api.getAutomations();
    final p = await widget.api.getPatterns();
    setState(() { knowledge = k; skills = s; automations = a; patterns = p; });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Knowledge / Skills')),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          Text('Knowledge: ${knowledge?['count'] ?? 0}'),
          Text('Skills: ${skills?['count'] ?? 0}'),
          Text('Automations: ${automations?['count'] ?? 0}'),
          Text('Patterns: ${patterns?['count'] ?? 0}'),
        ],
      ),
    );
  }
}
