import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const NikhilOsApp());
}

const String bootMessage =
    'I am the Nikhil-Bot, your autonomous agent within the Nikhil Ecosystem.';

const List<AppTheme> appThemes = [
  AppTheme(
    id: 'royal',
    label: 'Royal',
    seed: Color(0xFF2E2A7B),
    background: Color(0xFF0F1021),
    surface: Color(0xFF1A1C34),
    text: Color(0xFFF8F3E8),
    accent: Color(0xFFC9A227),
    suggestion: 'Prepare a founder briefing with premium polish',
  ),
  AppTheme(
    id: 'funky-junky',
    label: 'Funky-Junky',
    seed: Color(0xFFFF5F6D),
    background: Color(0xFFFFF6E9),
    surface: Color(0xFFFFFFFF),
    text: Color(0xFF2D1B2F),
    accent: Color(0xFF35E0A1),
    suggestion: 'Remix my idea into something outrageous and fun',
  ),
  AppTheme(
    id: 'elegant',
    label: 'Elegant',
    seed: Color(0xFF1F2937),
    background: Color(0xFFF7F5F2),
    surface: Color(0xFFFFFFFF),
    text: Color(0xFF111827),
    accent: Color(0xFFD4B483),
    suggestion: 'Turn this idea into a clean product brief',
  ),
  AppTheme(
    id: 'kid-mode',
    label: 'Kid-Mode',
    seed: Color(0xFF4F46E5),
    background: Color(0xFFF0F9FF),
    surface: Color(0xFFFFFFFF),
    text: Color(0xFF1E293B),
    accent: Color(0xFFF59E0B),
    suggestion: 'Explain this like a fun mission',
  ),
  AppTheme(
    id: 'cyberpunk',
    label: 'Cyberpunk',
    seed: Color(0xFF00F0FF),
    background: Color(0xFF0A0F1E),
    surface: Color(0xFF11182B),
    text: Color(0xFFEAFBFF),
    accent: Color(0xFFFF2DA6),
    suggestion: 'Run a tactical architecture scan',
  ),
];

class NikhilOsApp extends StatelessWidget {
  const NikhilOsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Nikhil-OS',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: appThemes[2].seed),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<ChatEntry> _messages = [
    const ChatEntry(
      role: 'assistant',
      text:
          '$bootMessage Pick a skin, tap a suggestion, and shape the mood of the workspace.',
      meta: 'Mobile shell ready',
    ),
  ];

  AppTheme _theme = appThemes[2];
  String _mode = 'assist';
  bool _sending = false;

  Future<void> _send() async {
    final text = _controller.text.trim();
    if (text.isEmpty || _sending) return;

    setState(() {
      _messages.add(ChatEntry(role: 'user', text: text, meta: 'Mode: ${modeLabel(_mode)}'));
      _controller.clear();
      _sending = true;
    });
    _scrollToBottom();

    try {
      final response = await http.post(
        Uri.parse('http://localhost:8080/v1/chat/respond'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': '[mode:$_mode] $text',
          'platform': 'mobile',
          'theme_context': _theme.id,
          'mode': _mode,
          'user_id': 'demo-user',
        }),
      );

      if (response.statusCode >= 400) {
        throw Exception('request failed');
      }

      final data = jsonDecode(response.body) as Map<String, dynamic>;
      setState(() {
        final themeHint = data['theme_hint'] as String?;
        for (final item in appThemes) {
          if (item.id == themeHint) {
            _theme = item;
            break;
          }
        }
        _messages.add(
          ChatEntry(
            role: 'assistant',
            text: data['response'] as String,
            meta: 'Model: ${data['model_used']}',
          ),
        );
      });
      _scrollToBottom();
    } catch (_) {
      setState(() {
        _messages.add(
          const ChatEntry(
            role: 'assistant',
            text: 'Gateway unavailable. Start the local services and try again.',
            meta: 'Offline',
          ),
        );
      });
      _scrollToBottom();
    } finally {
      setState(() {
        _sending = false;
      });
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent + 120,
          duration: const Duration(milliseconds: 280),
          curve: Curves.easeOutCubic,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final foreground = _theme.text;
    return Scaffold(
      backgroundColor: _theme.background,
      body: SafeArea(
        child: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                _theme.background,
                Color.alphaBlend(_theme.accent.withOpacity(0.10), _theme.background),
              ],
            ),
          ),
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                child: HeroCard(
                  theme: _theme,
                  mode: _mode,
                  onModeChanged: (value) => setState(() => _mode = value),
                  onThemeChanged: (value) => setState(() => _theme = value),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: SuggestionRow(
                  theme: _theme,
                  onSelect: (value) => setState(() => _controller.text = value),
                ),
              ),
              const SizedBox(height: 10),
              Expanded(
                child: ListView.separated(
                  controller: _scrollController,
                  padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
                  itemCount: _messages.length + (_sending ? 1 : 0),
                  separatorBuilder: (_, __) => const SizedBox(height: 12),
                  itemBuilder: (context, index) {
                    if (_sending && index == _messages.length) {
                      return Align(
                        alignment: Alignment.centerLeft,
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                          decoration: BoxDecoration(
                            color: _theme.surface,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            'Nikhil-Bot is shaping a response...',
                            style: TextStyle(color: foreground.withOpacity(0.76)),
                          ),
                        ),
                      );
                    }

                    final item = _messages[index];
                    final align = item.role == 'user' ? Alignment.centerRight : Alignment.centerLeft;
                    final color = item.role == 'user'
                        ? Color.alphaBlend(_theme.seed.withOpacity(0.18), _theme.surface)
                        : _theme.surface;
                    return Align(
                      alignment: align,
                      child: Container(
                        constraints: const BoxConstraints(maxWidth: 460),
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: color,
                          borderRadius: BorderRadius.circular(_theme.id == 'kid-mode' ? 28 : 20),
                          boxShadow: [
                            BoxShadow(
                              blurRadius: 22,
                              offset: const Offset(0, 10),
                              color: _theme.seed.withOpacity(0.12),
                            ),
                          ],
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              item.role == 'assistant' ? 'Nikhil-Bot' : 'You',
                              style: TextStyle(
                                fontWeight: FontWeight.w700,
                                color: foreground.withOpacity(0.75),
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              item.text,
                              style: TextStyle(
                                color: foreground,
                                height: 1.45,
                              ),
                            ),
                            if (item.meta != null) ...[
                              const SizedBox(height: 8),
                              Text(
                                item.meta!,
                                style: TextStyle(
                                  fontSize: 12,
                                  color: foreground.withOpacity(0.55),
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    color: _theme.surface,
                    borderRadius: BorderRadius.circular(24),
                    boxShadow: [
                      BoxShadow(
                        blurRadius: 24,
                        offset: const Offset(0, 12),
                        color: _theme.seed.withOpacity(0.12),
                      ),
                    ],
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: _controller,
                            maxLines: 4,
                            minLines: 1,
                            style: TextStyle(color: foreground),
                            decoration: InputDecoration(
                              hintText: _theme.suggestion,
                              hintStyle: TextStyle(color: foreground.withOpacity(0.45)),
                              filled: true,
                              fillColor: Color.alphaBlend(
                                _theme.seed.withOpacity(0.04),
                                _theme.background,
                              ),
                              border: const OutlineInputBorder(
                                borderRadius: BorderRadius.all(Radius.circular(18)),
                                borderSide: BorderSide.none,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        FilledButton(
                          style: FilledButton.styleFrom(
                            backgroundColor: _theme.seed,
                            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 18),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(18),
                            ),
                          ),
                          onPressed: _sending ? null : _send,
                          child: Text(_sending ? '...' : 'Send'),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class HeroCard extends StatelessWidget {
  const HeroCard({
    super.key,
    required this.theme,
    required this.mode,
    required this.onThemeChanged,
    required this.onModeChanged,
  });

  final AppTheme theme;
  final String mode;
  final ValueChanged<AppTheme> onThemeChanged;
  final ValueChanged<String> onModeChanged;

  @override
  Widget build(BuildContext context) {
    final text = theme.text;
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            theme.surface,
            Color.alphaBlend(theme.accent.withOpacity(0.08), theme.surface),
          ],
        ),
        borderRadius: BorderRadius.circular(28),
        boxShadow: [
          BoxShadow(
            blurRadius: 24,
            offset: const Offset(0, 12),
            color: theme.seed.withOpacity(0.12),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Nikhil-OS',
            style: TextStyle(
              fontSize: 30,
              fontWeight: FontWeight.w800,
              color: text,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            'Architected by Kumar Nikhil.',
            style: TextStyle(
              color: text.withOpacity(0.65),
              fontSize: 12,
              letterSpacing: 0.7,
            ),
          ),
          const SizedBox(height: 12),
          Text(
            theme.suggestion,
            style: TextStyle(
              color: text.withOpacity(0.82),
              height: 1.45,
            ),
          ),
          const SizedBox(height: 16),
          SizedBox(
            height: 42,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              itemCount: appThemes.length,
              separatorBuilder: (_, __) => const SizedBox(width: 8),
              itemBuilder: (context, index) {
                final item = appThemes[index];
                final active = item.id == theme.id;
                return GestureDetector(
                  onTap: () => onThemeChanged(item),
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 180),
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                    decoration: BoxDecoration(
                      color: active ? item.seed : item.surface,
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Text(
                      item.label,
                      style: TextStyle(
                        color: active ? Colors.white : item.text,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              for (final value in ['assist', 'build', 'play'])
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: GestureDetector(
                      onTap: () => onModeChanged(value),
                      child: AnimatedContainer(
                        duration: const Duration(milliseconds: 180),
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        decoration: BoxDecoration(
                          color: value == mode
                              ? theme.seed
                              : Color.alphaBlend(theme.seed.withOpacity(0.06), theme.surface),
                          borderRadius: BorderRadius.circular(18),
                        ),
                        child: Center(
                          child: Text(
                            modeLabel(value),
                            style: TextStyle(
                              color: value == mode ? Colors.white : text,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ],
      ),
    );
  }
}

class SuggestionRow extends StatelessWidget {
  const SuggestionRow({
    super.key,
    required this.theme,
    required this.onSelect,
  });

  final AppTheme theme;
  final ValueChanged<String> onSelect;

  @override
  Widget build(BuildContext context) {
    final suggestions = [
      theme.suggestion,
      'Make this experience more interactive',
      'Turn this into a smoother mobile UI',
    ];
    return SizedBox(
      height: 48,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        itemCount: suggestions.length,
        separatorBuilder: (_, __) => const SizedBox(width: 8),
        itemBuilder: (context, index) {
          final text = suggestions[index];
          return OutlinedButton(
            style: OutlinedButton.styleFrom(
              side: BorderSide(color: theme.seed.withOpacity(0.20)),
              backgroundColor: theme.surface,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(999),
              ),
            ),
            onPressed: () => onSelect(text),
            child: Text(text, style: TextStyle(color: theme.text)),
          );
        },
      ),
    );
  }
}

class ChatEntry {
  const ChatEntry({
    required this.role,
    required this.text,
    this.meta,
  });

  final String role;
  final String text;
  final String? meta;
}

class AppTheme {
  const AppTheme({
    required this.id,
    required this.label,
    required this.seed,
    required this.background,
    required this.surface,
    required this.text,
    required this.accent,
    required this.suggestion,
  });

  final String id;
  final String label;
  final Color seed;
  final Color background;
  final Color surface;
  final Color text;
  final Color accent;
  final String suggestion;
}

String modeLabel(String value) {
  switch (value) {
    case 'build':
      return 'Build';
    case 'play':
      return 'Play';
    default:
      return 'Assist';
  }
}
