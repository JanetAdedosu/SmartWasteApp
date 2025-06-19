import 'dart:io';
import 'dart:convert';
import 'dart:async';
import 'package:http/http.dart' as http;

class ModelInference {
  final String apiUrl = 'http://172.20.10.6:5001/classify';

  Future<String> runModelOnImage(String imagePath) async {
    try {
      final fileExists = await File(imagePath).exists();
      if (!fileExists) return '❌ Image not found: $imagePath';

      var request = http.MultipartRequest('POST', Uri.parse(apiUrl));
      request.files.add(await http.MultipartFile.fromPath('image', imagePath));

      final streamedResponse = await request.send().timeout(const Duration(seconds: 10));

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

}
