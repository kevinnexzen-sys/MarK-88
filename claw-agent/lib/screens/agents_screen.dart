import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AgentsScreen extends StatefulWidget {
  final ApiService api;
  const AgentsScreen({super.key, required this.api});

  @override
  State<AgentsScreen> createState() => _AgentsScreenState();
}

class _AgentsScreenState extends State<AgentsScreen> {
  List<dynamic> agents = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    refresh();
  }

  Future<void> refresh() async {
    final data = await widget.api.getAgents();
    if (!mounted) return;
    setState(() { agents = data; loading = false; });
  }

  @override
  Widget build(BuildContext context) {
    if (loading) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    return Scaffold(
      appBar: AppBar(title: const Text('Agents & Subagents')),
      body: RefreshIndicator(
        onRefresh: refresh,
        child: ListView(
          children: agents.map((a) => Card(
            child: ListTile(
              title: Text(a['name'] ?? 'Agent'),
              subtitle: Text('${a['role'] ?? ''} • ${a['status'] ?? ''}'),
            ),
          )).toList(),
        ),
      ),
    );
  }
}
