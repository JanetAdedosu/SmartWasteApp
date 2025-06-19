import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:camera/camera.dart';
import 'package:tflite/tflite.dart';

class SpeechScreen extends StatefulWidget {
  final List<CameraDescription> cameras;

  const SpeechScreen({Key? key, required this.cameras}) : super(key: key);

  @override
  _SpeechScreenState createState() => _SpeechScreenState();
}

class _SpeechScreenState extends State<SpeechScreen> {
  late stt.SpeechToText _speech;
  bool _isListening = false;
  String _text = 'Press the mic and start speaking...';
  CameraController? _cameraController;
  bool _isCameraInitialized = false;

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _initializeCamera();
    _loadModel();
  }

  void _initializeCamera() async {
    if (widget.cameras.isNotEmpty) {
      _cameraController = CameraController(
        widget.cameras[0],
        ResolutionPreset.medium,
      );
      try {
        await _cameraController!.initialize();
        if (!mounted) return;
        setState(() {
          _isCameraInitialized = true;
        });
      } catch (e) {
        print('Camera initialization error: $e');
      }
    } else {
      print('No cameras found');
    }
  }

  void _loadModel() async {
    String? result = await Tflite.loadModel(
      model: "assets/model.tflite",
      labels: "assets/labels.txt",
    );
    print("Model loaded: $result");
  }

  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize(
        onStatus: (val) => print('Status: $val'),
        onError: (val) => print('Error: $val'),
      );
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(
          onResult: (val) => setState(() {
            _text = val.recognizedWords;
          }),
        );
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
    }
  }

  void _classifyImage(String imagePath) async {
    var output = await Tflite.runModelOnImage(
      path: imagePath,
      numResults: 5,
      threshold: 0.5,
      asynch: true,
    );
    if (output != null && output.isNotEmpty) {
      String label = output[0]['label'];
      _showClassificationResult(label);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('No classification result'),
      ));
    }
  }

  void _showClassificationResult(String label) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Classification Result'),
          content: Text('This item is classified as: $label'),
          actions: [
            TextButton(
              child: Text('OK'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  void _takePicture() async {
    if (_cameraController == null || !_cameraController!.value.isInitialized) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Camera not ready yet.'),
      ));
      return;
    }

    try {
      final image = await _cameraController!.takePicture();
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Picture taken: ${image.path}'),
      ));
      _classifyImage(image.path);
    } catch (e) {
      print('Error taking picture: $e');
    }
  }

  @override
  void dispose() {
    _speech.stop();
    _cameraController?.dispose();
    Tflite.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart Waste Sorting 🗣️📸'),
        backgroundColor: Colors.green,
      ),
      body: SingleChildScrollView(
        child: Container(
          padding: const EdgeInsets.all(20),
          color: Colors.purple.shade50,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.mic,
                size: 80,
                color: _isListening ? Colors.red : Colors.grey,
              ),
              const SizedBox(height: 20),
              Text(
                _text,
                style: const TextStyle(fontSize: 20),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),
              _isCameraInitialized && _cameraController != null
                  ? SizedBox(
                      height: 200,
                      child: CameraPreview(_cameraController!),
                    )
                  : const CircularProgressIndicator(),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: _takePicture,
                icon: const Icon(Icons.camera_alt),
                label: const Text('Take Picture'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green,
                  foregroundColor: Colors.white,
                ),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _listen,
        backgroundColor: Colors.green,
        child: Icon(
          _isListening ? Icons.mic : Icons.mic_none,
          color: Colors.white,
          size: 30,
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}
