import 'package:flutter/material.dart';
import 'services/api_service.dart';
import 'screens/dashboard.dart';
import 'screens/settings_screen.dart';
import 'screens/pc_control_screen.dart';
import 'screens/knowledge_screen.dart';
import 'screens/preview_screen.dart';
import 'screens/approvals_screen.dart';
import 'screens/agents_screen.dart';
import 'screens/voice_screen.dart';

void main() {
  runApp(const ClawApp());
}

class ClawApp extends StatefulWidget {
  const ClawApp({super.key});

  @override
  State<ClawApp> createState() => _ClawAppState();
}

class _ClawAppState extends State<ClawApp> {
  final api = ApiService();
  bool ready = false;

  @override
  void initState() {
    super.initState();
    _boot();
  }

  Future<void> _boot() async {
    await api.login('admin', 'admin123');
    setState(() => ready = true);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CLAW',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.blue),
      home: !ready ? const Scaffold(body: Center(child: CircularProgressIndicator())) : HomeShell(api: api),
    );
  }
}

class HomeShell extends StatefulWidget {
  final ApiService api;
  const HomeShell({super.key, required this.api});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  int index = 0;

  @override
  Widget build(BuildContext context) {
    final screens = [
      DashboardScreen(api: widget.api),
      ApprovalsScreen(api: widget.api),
      AgentsScreen(api: widget.api),
      KnowledgeScreen(api: widget.api),
      PreviewScreen(api: widget.api),
      VoiceScreen(api: widget.api),
      PCControlScreen(api: widget.api),
      SettingsScreen(api: widget.api),
    ];
    return Scaffold(
      body: screens[index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (v) => setState(() => index = v),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.dashboard), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.fact_check), label: 'Approvals'),
          NavigationDestination(icon: Icon(Icons.hub), label: 'Agents'),
          NavigationDestination(icon: Icon(Icons.psychology), label: 'Knowledge'),
          NavigationDestination(icon: Icon(Icons.preview), label: 'Preview'),
          NavigationDestination(icon: Icon(Icons.mic), label: 'Voice'),
          NavigationDestination(icon: Icon(Icons.computer), label: 'PC'),
          NavigationDestination(icon: Icon(Icons.settings), label: 'Settings'),
        ],
      ),
    );
  }
}
