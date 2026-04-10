class InvoiceAgent:
    def run(self, payload: dict):
        return {"agent": "InvoiceAgent", "status": "ok", "payload": payload}
