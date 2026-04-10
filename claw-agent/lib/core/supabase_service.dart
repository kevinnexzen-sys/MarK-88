class SupabaseService {
  final String url;
  final String anonKey;
  SupabaseService({required this.url, required this.anonKey});

  bool get configured => url.isNotEmpty && anonKey.isNotEmpty;
}
