import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'ml/model_inference.dart';

class SpeechScreen extends StatefulWidget {
  final List<CameraDescription> cameras;

   


  const SpeechScreen({Key? key,  required this.cameras}) : super(key: key);
  @override
  _SpeechScreenState createState() => _SpeechScreenState();
  }

 class _SpeechScreenState extends State<SpeechScreen> {
  late CameraController _cameraController;
  late stt.SpeechToText _speech;
  late ModelInference _modelInference;

  bool _isCameraInitialized = false;
  bool _isListening = false;
  bool _isProcessingImage = false;
  String _speechText = '';
  String? _classificationResult;

  @override
void initState() {
  super.initState();
  _speech = stt.SpeechToText();
  _modelInference = ModelInference();
  _initializeCamera();
}


  



@override
void dispose() {
  _cameraController.dispose();
  _speech.stop();
  _modelInference.close();
  super.dispose();
}

Future<void> _initializeCamera() async {
  if (widget.cameras.isEmpty) return;

  _cameraController = CameraController(widget.cameras[0],
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
    if (val.recognizedWords.toLowerCase().contains("classify") || 
    val.recognizedWords.toLowerCase().contains("sort this waste")) {
 {
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



Future<void> _takePictureAndClassify() async {
  if (!_isCameraInitialized || _isProcessingImage) return;

  setState(() {
    _isProcessingImage = true;
    _classificationResult = null;
  });

  try {
    final imageFile = await _cameraController.takePicture();
    // Placeholder result:
    final result = await _modelInference.runModelOnImage(imageFile.path);
    setState(() {
      _classificationResult = result;
      _isProcessingImage = false;
    });
  } catch (e) {
    print('Error: $e');
    setState(() {
      _classificationResult = '❌ Classification failed';
      _isProcessingImage = false;
    });
  }
}




  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Smart Waste App')),
        body: SingleChildScrollView(
  padding: const EdgeInsets.all(12),
  child: Column(
    children: [
      if (_isCameraInitialized && _cameraController.value.isInitialized)
        AspectRatio(
          aspectRatio: _cameraController.value.aspectRatio,
          child: CameraPreview(_cameraController),
        )
      else
        const CircularProgressIndicator(),

      const SizedBox(height: 20),
      Text(
        _speechText.isEmpty ? 'Say something...' : _speechText,
        style: const TextStyle(fontSize: 20),
      ),

      const SizedBox(height: 30),
      FloatingActionButton(
        onPressed: _isListening ? _stopListening : _startListening,
        child: Icon(_isListening ? Icons.mic : Icons.mic_none),
      ),
    ],
  ),
),



);

}

}