import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'speech_screen.dart';

List<CameraDescription> cameras = [];

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras();
  runApp(const SmartWasteApp());
}

class SmartWasteApp extends StatelessWidget {
  const SmartWasteApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Waste App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: SpeechScreen(cameras: cameras), // 👈 PASS CAMERAS
    );
  }
}
