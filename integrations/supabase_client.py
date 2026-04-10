class SupabaseClientState:
    def __init__(self, url: str = "", anon_key: str = "", service_key: str = ""):
        self.url = url
        self.anon_key = anon_key
        self.service_key = service_key

    def configured(self):
        return bool(self.url and (self.anon_key or self.service_key))

    def health(self):
        return {"configured": self.configured(), "url_present": bool(self.url)}
