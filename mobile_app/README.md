# Crop Disease Detection Mobile App

This is a Flutter-based mobile application that allows farmers to upload crop images and receive pest/disease diagnoses.

## Features

- Upload crop images from camera or gallery
- Optionally enter crop name
- View pest/disease detection results
- View detailed diagnosis and treatment recommendations
- View history of previous detections

## Setup

1. Install Flutter: https://flutter.dev/docs/get-started/install
2. Clone this repository
3. Run `flutter pub get` to install dependencies
4. Update the API endpoint in `lib/services/api_service.dart`
5. Run the app: `flutter run`

## Project Structure

```
mobile_app/
├── lib/
│   ├── main.dart
│   ├── models/
│   │   └── detection_result.dart
│   ├── screens/
│   │   ├── home_screen.dart
│   │   ├── upload_screen.dart
│   │   └── result_screen.dart
│   ├── services/
│   │   └── api_service.dart
│   └── widgets/
│       ├── image_picker_widget.dart
│       └── result_card_widget.dart
├── pubspec.yaml
└── README.md
```

## Implementation

To implement this mobile app, you would need to:

1. Set up a new Flutter project
2. Create the models, screens, services, and widgets as outlined above
3. Implement the API service to communicate with the FastAPI backend
4. Build the UI for image upload, result display, and history viewing

## Sample API Integration

```dart
class ApiService {
  final String baseUrl = 'https://your-api-url.com/api';
  final dio = Dio();

  Future<DetectionResult> uploadImage(File image, String? cropName) async {
    try {
      FormData formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(image.path),
        if (cropName != null) 'crop_name': cropName,
      });

      final response = await dio.post('$baseUrl/upload', data: formData);
      return DetectionResult.fromJson(response.data);
    } catch (e) {
      throw Exception('Failed to upload image: $e');
    }
  }

  Future<List<DetectionResult>> getHistory() async {
    try {
      final response = await dio.get('$baseUrl/history');
      return (response.data as List)
          .map((json) => DetectionResult.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Failed to get history: $e');
    }
  }
}
```

## Next Steps

To complete the mobile app implementation:

1. Create the Flutter project structure
2. Implement the UI screens and widgets
3. Connect to the FastAPI backend
4. Add image picking functionality
5. Implement result display and history viewing
6. Add offline support and caching
7. Optimize for different screen sizes and orientations