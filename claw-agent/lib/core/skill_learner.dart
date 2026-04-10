class SkillLearner {
  Map<String, dynamic> createSkillSuggestion(String topic, String learnedSummary) {
    return {"topic": topic, "summary": learnedSummary, "status": "suggested"};
  }
}
