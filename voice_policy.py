def get_voice_policy():
    return {
        "desktop_listen_only": True,
        "mobile_speaks": True,
        "mobile_voice_style": "natural_human_like",
        "desktop_speaks": False,
        "rule": "listen_on_both_speak_only_on_mobile",
    }
