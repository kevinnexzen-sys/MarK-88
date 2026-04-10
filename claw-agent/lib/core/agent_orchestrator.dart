class AgentOrchestrator {
  String selectProvider({required bool requiresOnline, required String mode}) {
    if (requiresOnline) return "openai";
    if (mode == "privacy") return "local";
    return "local";
  }
}
