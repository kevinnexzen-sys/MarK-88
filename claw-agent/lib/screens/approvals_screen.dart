import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ApprovalsScreen extends StatefulWidget {
  final ApiService api;
  const ApprovalsScreen({super.key, required this.api});

  @override
  State<ApprovalsScreen> createState() => _ApprovalsScreenState();
}

class _ApprovalsScreenState extends State<ApprovalsScreen> {
  List<dynamic> rows = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    refresh();
  }

  Future<void> refresh() async {
    final data = await widget.api.getApprovals();
    if (!mounted) return;
    setState(() { rows = data; loading = false; });
  }

  Future<void> act(int taskId, bool approve) async {
    await widget.api.approveTask(taskId, approve: approve);
    await refresh();
  }

  @override
  Widget build(BuildContext context) {
    if (loading) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    return Scaffold(
      appBar: AppBar(title: const Text('Approvals')),
      body: RefreshIndicator(
        onRefresh: refresh,
        child: ListView(
          children: rows.map((r) => Card(
            child: ListTile(
              title: Text(r['summary'] ?? 'Approval'),
              subtitle: Text('Task ${r['task_id']} • ${r['status']}'),
              trailing: Wrap(spacing: 8, children: [
                IconButton(onPressed: () => act(r['task_id'], true), icon: const Icon(Icons.check_circle)),
                IconButton(onPressed: () => act(r['task_id'], false), icon: const Icon(Icons.cancel)),
              ]),
            ),
          )).toList(),
        ),
      ),
    );
  }
}
