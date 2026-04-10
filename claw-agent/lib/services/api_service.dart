import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  String baseUrl = 'http://10.0.2.2:8787';
  String? token;

  Map<String, String> _headers() => {
    'Content-Type': 'application/json',
    if (token != null) 'Authorization': 'Bearer $token',
  };

  Future<bool> login(String username, String password) async {
    final r = await http.post(
      Uri.parse('$baseUrl/api/auth/login'),
      headers: _headers(),
      body: jsonEncode({'username': username, 'password': password}),
    );
    if (r.statusCode == 200) {
      token = jsonDecode(r.body)['token'];
      return true;
    }
    return false;
  }

  Future<void> mobileEvent(String eventType, String payload, {int confidence = 70}) async {
    await http.post(Uri.parse('$baseUrl/api/learning/mobile-event'), headers: _headers(), body: jsonEncode({'event_type': eventType, 'payload': payload, 'confidence': confidence}));
  }

  Future<Map<String, dynamic>> getSummary() async => _get('/api/dashboard/summary');
  Future<List<dynamic>> getApprovals() async => _getList('/api/dashboard/approvals');
  Future<List<dynamic>> getAgents() async => _getList('/api/agents');
  Future<Map<String, dynamic>> getProviderStatus() async => _get('/api/providers/status');
  Future<Map<String, dynamic>> getVoicePolicy() async => _get('/api/voice/policy');
  Future<List<dynamic>> getKnowledge() async => _getList('/api/dashboard/knowledge');
  Future<List<dynamic>> getInstructions() async => _getList('/api/dashboard/instructions');
  Future<List<dynamic>> getPreviews() async => _getList('/api/dashboard/previews');
  Future<Map<String, dynamic>> getFinancials() async => _get('/api/dashboard/financials');
  Future<Map<String, dynamic>> getLearningGraph() async => _get('/api/learning/graph');
  Future<List<dynamic>> getPatterns() async => _getList('/api/learning/patterns');
  Future<List<dynamic>> getSkills() async => _getList('/api/dashboard/skills');
  Future<List<dynamic>> getAutomations() async => _getList('/api/dashboard/automations');
  Future<List<dynamic>> getWorkers() async => _getList('/api/workers');
  Future<List<dynamic>> getDevices() async => _getList('/api/devices');
  Future<List<dynamic>> getTasks() async => _getList('/api/dashboard/tasks');
  Future<List<dynamic>> getCommands() async => _getList('/api/dashboard/commands');
  Future<List<dynamic>> getMemory() async => _getList('/api/memory');

  Future<Map<String, dynamic>> approveTask(int taskId, {bool approve = true}) async {
    final endpoint = approve
        ? '$baseUrl/api/approvals/task/$taskId/approve'
        : '$baseUrl/api/approvals/task/$taskId/reject';
    final r = await http.post(Uri.parse(endpoint), headers: _headers());
    return jsonDecode(r.body);
  }

  Future<Map<String, dynamic>> createTask(Map<String, dynamic> payload) async {
    final r = await http.post(
      Uri.parse('$baseUrl/api/tasks'),
      headers: _headers(),
      body: jsonEncode(payload),
    );
    return jsonDecode(r.body);
  }

  Future<Map<String, dynamic>> interpretCommand(String text) async {
    final r = await http.post(
      Uri.parse('$baseUrl/api/commands/interpret'),
      headers: _headers(),
      body: jsonEncode({'text': text, 'source': 'mobile_voice'}),
    );
    return jsonDecode(r.body);
  }

  Future<Map<String, dynamic>> runtimeTick() async {
    final r = await http.post(Uri.parse('$baseUrl/api/runtime/tick'), headers: _headers());
    return jsonDecode(r.body);
  }

  Future<Map<String, dynamic>> wakeDevice(int deviceId) async {
    final r = await http.post(Uri.parse('$baseUrl/api/devices/$deviceId/wake'), headers: _headers());
    return jsonDecode(r.body);
  }

  Future<Map<String, dynamic>> _get(String path) async {
    final r = await http.get(Uri.parse('$baseUrl$path'), headers: _headers());
    return jsonDecode(r.body);
  }

  Future<List<dynamic>> _getList(String path) async {
    final r = await http.get(Uri.parse('$baseUrl$path'), headers: _headers());
    return jsonDecode(r.body) as List<dynamic>;
  }
}
