class ApprovalGatekeeper:
    def run(self, payload: dict):
        return {"agent": "ApprovalGatekeeper", "status": "ok", "payload": payload}
