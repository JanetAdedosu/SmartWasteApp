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

      final streamedResponse = await request.send();
      final responseBody = await streamedResponse.stream.bytesToString();

      if (streamedResponse.statusCode == 200) {
        final json = jsonDecode(responseBody);
        return json['class']; // basic response
      } else {
        return '❌ Server error ${streamedResponse.statusCode}';
      }

    } catch (e) {
      return '❌ Unexpected error: $e';
    }
  }
  
}
