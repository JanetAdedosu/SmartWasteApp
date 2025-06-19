import 'dart:convert';
import 'dart:async';
import 'dart:io';
import 'package:http/http.dart' as http;

class ModelInference {
  final String apiUrl = 'http://172.20.10.6:5001/classify'; // ✅ Adjust this to match your backend IP

  Future<String> runModelOnImage(String imagePath) async {
    try {
      final fileExists = await File(imagePath).exists();
      if (!fileExists) return '❌ Image not found: $imagePath';

      var request = http.MultipartRequest('POST', Uri.parse(apiUrl));
      request.files.add(await http.MultipartFile.fromPath('image', imagePath));

      final streamedResponse = await request.send().timeout(const Duration(seconds: 10));
      final responseBody = await streamedResponse.stream.bytesToString();

      if (streamedResponse.statusCode == 200) {
        final json = jsonDecode(responseBody);
        final label = json['class'];
        final confidence = (json['confidence'] as num).toDouble() * 100;

        final bin = _germanBin(label);
        return "$label (${confidence.toStringAsFixed(2)}%) ➜ Bin: $bin";
      } else {
        return '❌ Server error ${streamedResponse.statusCode}';
      }
    } on SocketException {
      return '❌ Network error.';
    } on TimeoutException {
      return '❌ Request timed out.';
    } on FormatException {
      return '❌ Invalid response.';
    } catch (e) {
      return '❌ Unexpected error: $e';
    }
  }

  String _germanBin(String label) {
    switch (label.toLowerCase()) {
      case 'organic':
        return 'Biotonne (Green)';
      case 'recyclable':
        return 'Gelbe Tonne (Yellow)';
      case 'plastic':
        return 'Plastikmüll (Yellow)';
      default:
        return 'Restmüll (Black)';
    }
  }

  void close() {
    // No resources to release
  }
}
