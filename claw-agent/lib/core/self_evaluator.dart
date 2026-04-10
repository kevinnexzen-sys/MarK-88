class SelfEvaluator {
  Map<String, dynamic> score({required int approvals, required int automationsAccepted}) {
    final score = (50 + approvals * 2 + automationsAccepted * 3).clamp(0, 100);
    return {"score": score};
  }
}
