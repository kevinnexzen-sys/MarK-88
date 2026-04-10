import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../core/voice_service.dart';

class VoiceScreen extends StatefulWidget {
  final ApiService api;
  const VoiceScreen({super.key, required this.api});

  @override
  State<VoiceScreen> createState() => _VoiceScreenState();
}

class _VoiceScreenState extends State<VoiceScreen> {
  final voice = VoiceService();
  String heard = "";
  String result = "";
  bool busy = false;

  Future<void> _listenAndSend() async {
    setState(() => busy = true);
    final text = await voice.listenOnce();
    if (!mounted) return;
    setState(() => heard = text);
    if (text.isNotEmpty) {
      final response = await widget.api.interpretCommand(text);
      result = "Task #${response['task_id']} created as ${response['status']}";
      await voice.speakMobile(result);
      if (mounted) setState(() {});
    }
    if (mounted) setState(() => busy = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Voice Command')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            FilledButton.icon(
              onPressed: busy ? null : _listenAndSend,
              icon: const Icon(Icons.mic),
              label: Text(busy ? 'Listening...' : 'Speak command'),
            ),
            const SizedBox(height: 16),
            Text('Heard: $heard'),
            const SizedBox(height: 12),
            Text('Result: $result'),
          ],
        ),
      ),
    );
  }
}
