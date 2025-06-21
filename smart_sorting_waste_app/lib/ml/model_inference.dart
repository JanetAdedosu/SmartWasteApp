import 'dart:io';
import 'dart:convert';
import 'dart:async';
import 'package:http/http.dart' as http;

class ModelInference {
  // API URL: Update this to your actual backend URL (if it's deployed)
  final String apiUrl = 'https://smartwasteapp-53.onrender.com/classify'; // Updated to production URL

  // Function to run inference on the image
  Future<String> runModelOnImage(String imagePath) async {
    try {
      // Check if the image file exists
      final fileExists = await File(imagePath).exists();
      if (!fileExists) return '❌ Image not found: $imagePath';

      // Create multipart request
      var request = http.MultipartRequest('POST', Uri.parse(apiUrl));

      // Add image file to request
      //request.files.add(await http.MultipartFile.fromPath('image', imagePath));
      //request.files.add(await http.MultipartFile.fromPath('file', imagePath));
      request.files.add(await http.MultipartFile.fromPath('image', imagePath));


      // Send the request with a timeout of 15 seconds (in case of large image uploads)
      final streamedResponse = await request.send().timeout(const Duration(seconds: 15));
      final responseBody = await streamedResponse.stream.bytesToString();

      // Handle server response
      if (streamedResponse.statusCode == 200) {
        final json = jsonDecode(responseBody);
        final label = json['class'];
        final confidence = (json['confidence'] as num).toDouble() * 100;

        final bin = _germanBin(label);
        return "$label (${confidence.toStringAsFixed(2)}%) ➜ Bin: $bin";
      } else {
        // Print the response body for debugging
        print('Server error response: $responseBody');
        return '❌ Server error ${streamedResponse.statusCode}';
      }
    } on SocketException {
      // Handle network error
      return '❌ Network error.';
    } on TimeoutException {
      // Handle request timeout
      return '❌ Request timed out.';
    } on FormatException {
      // Handle invalid response format
      return '❌ Invalid response format.';
    } catch (e) {
      // Catch any other unexpected errors
      return '❌ Unexpected error: $e';
    }
  }

  // Function to determine the German waste bin type based on the label
  String _germanBin(String label) {
    switch (label.toLowerCase()) {
      case 'organic':
        return 'Biotonne (Brown/Green)';
      case 'plastic':
      case 'recyclable':
        return 'Gelbe Tonne (Yellow)';
      case 'paper':
        return 'Blaue Tonne (Blue)';
      case 'glass':
        return 'Altglascontainer';
      default:
        return 'Restmüll (Black)';
    }
  }

  // Close function to clean up resources (no resources to release in this case)
  void close() {
    // No resources to release
  }
}
