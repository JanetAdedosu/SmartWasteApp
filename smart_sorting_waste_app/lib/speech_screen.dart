import 'package:flutter/material.dart';

class SpeechScreen extends StatelessWidget {
  const SpeechScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Smart Waste App')),
      body: const Center(
        child: Text('Initializing...'),
      ),
    );
  }
}
