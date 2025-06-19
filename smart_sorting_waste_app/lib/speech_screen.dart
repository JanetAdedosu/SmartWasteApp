import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

class SpeechScreen extends StatelessWidget {
  final List<CameraDescription> cameras;

  late stt.SpeechToText _speech;


  const SpeechScreen({Key? key required this.cameras}) : super(key: key);
  @override
  _SpeechScreenState createState() => _SpeechScreenState();
}

 class _SpeechScreenState extends State<SpeechScreen> {
  bool _isListening = false;
String _speechText = '';

  @override
void initState() {
  super.initState();
  _speech = stt.SpeechToText();
  _initializeCamera();
}


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
void _startListening() async {
  bool available = await _speech.initialize(
    onStatus: (val) => print('Speech status: $val'),
    onError: (val) => print('Speech error: $val'),
  );

  if (available) {
    setState(() => _isListening = true);
    _speech.listen(
  onResult: (val) {
    setState(() => _speechText = val.recognizedWords);
    if (val.recognizedWords.toLowerCase().contains("classify")) {
      _takePictureAndClassify();
    }
  },
);
  } else {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Speech recognition unavailable')),
    );
  }
}

void _stopListening() {
  _speech.stop();
  setState(() => _isListening = false);
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
     Text(
      _speechText.isEmpty ? 'Say something...' : _speechText,
      style: const TextStyle(fontSize: 20),
),
FloatingActionButton(
  onPressed: _isListening ? _stopListening : _startListening,
  child: Icon(_isListening ? Icons.mic : Icons.mic_none),
),


      
    );
  }
}



