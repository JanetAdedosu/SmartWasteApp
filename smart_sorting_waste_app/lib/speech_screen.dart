import 'package:flutter/material.dart';
import 'package:camera/camera.dart';

class SpeechScreen extends StatelessWidget {
  final List<CameraDescription> cameras;


  const SpeechScreen({Key? key required this.cameras}) : super(key: key);
  @override
  _SpeechScreenState createState() => _SpeechScreenState();
}

 class _SpeechScreenState extends State<SpeechScreen> {
  late CameraController _cameraController;
bool _isCameraInitialized = false;

@override
void initState() {
  super.initState();
  _initializeCamera();
}

@override
void dispose() {
  _cameraController.dispose();
  super.dispose();
}

Future<void> _initializeCamera() async {
  if (widget.cameras.isEmpty) return;

  _cameraController = CameraController(
    widget.cameras[0],
    ResolutionPreset.medium,
  );
  try {
    await _cameraController.initialize();
    setState(() => _isCameraInitialized = true);
  } catch (e) {
    print("Camera error: $e");
  }
}
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Smart Waste App')),
        body: Center(
  child: _isCameraInitialized
      ? AspectRatio(
          aspectRatio: _cameraController.value.aspectRatio,
          child: CameraPreview(_cameraController),
        )
       : const CircularProgressIndicator(),
     ),
      
    );
  }
}



