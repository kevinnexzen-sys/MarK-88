import 'package:flutter_tts/flutter_tts.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

class VoiceService {
  final FlutterTts tts = FlutterTts();
  final stt.SpeechToText speech = stt.SpeechToText();

  Future<void> configureMobileVoice() async {
    await tts.setLanguage("en-US");
    await tts.setSpeechRate(0.45);
    await tts.setPitch(1.0);
  }

  Future<String> listenOnce() async {
    final ok = await speech.initialize();
    if (!ok) return "";
    String text = "";
    await speech.listen(onResult: (r) => text = r.recognizedWords, listenFor: const Duration(seconds: 8));
    await Future.delayed(const Duration(seconds: 9));
    await speech.stop();
    return text;
  }

  Future<void> speakMobile(String text) async {
    await configureMobileVoice();
    await tts.speak(text);
  }
}
