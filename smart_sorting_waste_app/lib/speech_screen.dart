import 'package:flutter/material.dart';
import 'package:camera/camera.dart';

class SpeechScreen extends StatelessWidget {
  final List<CameraDescription> cameras;


  const SpeechScreen({Key? key}) : super(key: key);
  @override
  _SpeechScreenState createState() => _SpeechScreenState();
}

 class _SpeechScreenState extends State<SpeechScreen> {
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
