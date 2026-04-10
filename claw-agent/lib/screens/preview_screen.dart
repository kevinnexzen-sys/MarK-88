import 'package:flutter/material.dart';
import '../services/api_service.dart';

class PreviewScreen extends StatefulWidget {
  final ApiService api;
  const PreviewScreen({super.key, required this.api});

  @override
  State<PreviewScreen> createState() => _PreviewScreenState();
}

class _PreviewScreenState extends State<PreviewScreen> {
  Map<String, dynamic>? previews;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    final data = await widget.api.getPreviews();
    if (mounted) {
      setState(() {
        previews = data;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final items = previews?['items'] as List<dynamic>? ?? [];
    final left = items.isNotEmpty ? '${items.first['left_content'] ?? ''}' : '';
    final right = items.isNotEmpty ? '${items.first['right_content'] ?? ''}' : '';
    return Scaffold(
      appBar: AppBar(title: const Text('Preview')),
      body: Row(
        children: [
          Expanded(child: Container(padding: const EdgeInsets.all(12), color: Colors.grey.shade200, child: Text('Left preview\n$left'))),
          Expanded(child: Container(padding: const EdgeInsets.all(12), child: Text('Right preview\n$right'))),
        ],
      ),
    );
  }
}
