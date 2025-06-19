import 'package:flutter/material.dart';

void main() {
  runApp(SmartWasteApp());
}

class SmartWasteApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Waste App',
      theme: ThemeData(primarySwatch: Colors.green),
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Center(child: Text('Hello World')),
      ),
    );
  }
}





