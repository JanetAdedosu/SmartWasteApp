// import 'dart:io';
// import 'dart:convert';
// import 'dart:async';
// import 'package:http/http.dart' as http;

// class ModelInference {
//   // API URL: Update this to your actual backend URL (if it's deployed)
//   //final String apiUrl = 'https://smartwasteapp-4chk.onrender.com/classify'; // Updated to production URL
//   final String apiUrl = 'https://smartwasteapp-25.onrender.com/classify';

//   // Function to run inference on the image
//   Future<String> runModelOnImage(String imagePath) async {
//     try {
//       // Check if the image file exists
//       final fileExists = await File(imagePath).exists();
//       if (!fileExists) return '❌ Image not found: $imagePath';

//       // Create multipart request
//       var request = http.MultipartRequest('POST', Uri.parse(apiUrl));

//       // Add image file to request
//       //request.files.add(await http.MultipartFile.fromPath('image', imagePath));
//       //request.files.add(await http.MultipartFile.fromPath('file', imagePath));
//       request.files.add(await http.MultipartFile.fromPath('image', imagePath));


//       // Send the request with a timeout of 15 seconds (in case of large image uploads)
//       final streamedResponse = await request.send().timeout(const Duration(seconds: 15));
//       final responseBody = await streamedResponse.stream.bytesToString();

//       // Handle server response
//       if (streamedResponse.statusCode == 200) {
//         final json = jsonDecode(responseBody);
//         final label = json['class'];
//         final confidence = (json['confidence'] as num).toDouble() * 100;

//         final bin = _germanBin(label);
//         return "$label (${confidence.toStringAsFixed(2)}%) ➜ Bin: $bin";
//       } else {
//         // Print the response body for debugging
//         print('Server error response: $responseBody');
//         return '❌ Server error ${streamedResponse.statusCode}';
//       }
//     } on SocketException {
//       // Handle network error
//       return '❌ Network error.';
//     } on TimeoutException {
//       // Handle request timeout
//       return '❌ Request timed out.';
//     } on FormatException {
//       // Handle invalid response format
//       return '❌ Invalid response format.';
//     } catch (e) {
//       // Catch any other unexpected errors
//       return '❌ Unexpected error: $e';
//     }
//   }

//   String _germanBin(String label) {
//   final normalized = label.trim().toLowerCase();

//   const bins = {
//     'Organic': 'Biotonne (Brown/Green)',
//     'Plastic': 'Gelbe Tonne (Yellow)',
//     'Paper': 'Blaue Tonne (Blue)',
//   };

//   return bins[normalized] ?? 'Unbekannt';
// }



//   // Close function to clean up resources (no resources to release in this case)
//   void close() {
//     // No resources to release
//   }
// }


// import 'dart:io';
// import 'dart:convert';
// import 'dart:async';
// import 'package:http/http.dart' as http;

// class ModelInference {
//   // Backend API URL
//   final String apiUrl = 'https://smartwasteapp-25.onrender.com/classify';

//   // Run inference on a local image
//   Future<String> runModelOnImage(String imagePath) async {
//     try {
//       // Check if file exists
//       final fileExists = await File(imagePath).exists();
//       if (!fileExists) return '❌ Image not found: $imagePath';

//       // Create multipart request
//       var request = http.MultipartRequest('POST', Uri.parse(apiUrl));
//       request.files.add(await http.MultipartFile.fromPath('image', imagePath));

//       // Send request
//       final streamedResponse =
//           await request.send().timeout(const Duration(seconds: 15));
//       final responseBody = await streamedResponse.stream.bytesToString();

//       if (streamedResponse.statusCode == 200) {
//         final json = jsonDecode(responseBody);
//         final label = (json['class'] as String).trim().toLowerCase();
//         final confidence = (json['confidence'] as num).toDouble() * 100;

//         final bin = _germanBin(label);
//         return "$label (${confidence.toStringAsFixed(2)}%) ➜ Bin: $bin";
//       } else {
//         print('Server error response: $responseBody');
//         return '❌ Server error ${streamedResponse.statusCode}';
//       }
//     } on SocketException {
//       return '❌ Network error.';
//     } on TimeoutException {
//       return '❌ Request timed out.';
//     } on FormatException {
//       return '❌ Invalid response format.';
//     } catch (e) {
//       return '❌ Unexpected error: $e';
//     }
//   }

//   // Map class label to German bin
//   String _germanBin(String label) {
//     const bins = {
//       'organic': 'Biotonne (Brown/Green)',
//       'plastic': 'Gelbe Tonne (Yellow)',
//       'paper': 'Blaue Tonne (Blue)',
//     };
//     // Guaranteed to find a bin because backend always returns a valid label
//     return bins[label]!;
//   }

//   void close() {}
// }


import 'dart:io';
import 'dart:convert';
import 'dart:async';
import 'package:http/http.dart' as http;

class ModelInference {
  // Backend API URL
  final String apiUrl = 'https://smartwasteapp-48.onrender.com/classify';

  // Run inference on a local image
  Future<String> runModelOnImage(String imagePath) async {
    try {
      // Check if file exists
      final fileExists = await File(imagePath).exists();
      if (!fileExists) return '❌ Image not found: $imagePath';

      // Create multipart request
      var request = http.MultipartRequest('POST', Uri.parse(apiUrl));
      request.files.add(await http.MultipartFile.fromPath('image', imagePath));

      // Send request
      final streamedResponse =
          await request.send().timeout(const Duration(seconds: 15));
      final responseBody = await streamedResponse.stream.bytesToString();

      if (streamedResponse.statusCode == 200) {
        final json = jsonDecode(responseBody);

        // Original label from backend (keeps capitalization)
        final originalLabel = (json['class'] as String).trim();

        // Lowercase version for mapping
        final lowerLabel = originalLabel.toLowerCase();

        final confidence = (json['confidence'] as num).toDouble() * 100;

        // Get German bin name with emoji
        final bin = _germanBin(lowerLabel);

        return "$originalLabel (${confidence.toStringAsFixed(2)}%) ➜ $bin";
      } else {
        print('Server error response: $responseBody');
        return '❌ Server error ${streamedResponse.statusCode}';
      }
    } on SocketException {
      return '❌ Network error.';
    } on TimeoutException {
      return '❌ Request timed out.';
    } on FormatException {
      return '❌ Invalid response format.';
    } catch (e) {
      return '❌ Unexpected error: $e';
    }
  }

  // Map class label to German bin with emojis
  String _germanBin(String label) {
    const bins = {
      'organic': 'Biotonne (Brown/Green) 🟩',
      'plastic': 'Gelbe Tonne (Yellow) 🟨',
      'paper': 'Blaue Tonne (Blue) 🟦',
    };
    return bins[label] ?? 'Unbekannt ❓';
  }

  void close() {}
}
