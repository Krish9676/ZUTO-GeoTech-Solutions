# Crop Disease Detection Mobile App

A Flutter mobile application for detecting crop diseases using AI. Users can upload images of crops and receive instant disease detection results.

## 🚀 Features

- **User Authentication**: Secure login and signup with Supabase
- **Image Upload**: Capture or select images from gallery
- **AI Detection**: Upload images for instant disease detection
- **History**: View all previous detection results
- **Detailed Results**: See confidence scores, diagnoses, and heatmaps
- **Modern UI**: Beautiful, responsive design with Material 3

## 📱 Screens

1. **Splash Screen** - App introduction
2. **Login Screen** - User authentication
3. **Signup Screen** - Account creation
4. **Home Screen** - Main dashboard with detection history
5. **Upload Screen** - Image capture and upload
6. **Result Screen** - Detailed detection results

## 🛠️ Tech Stack

- **Framework**: Flutter 3.x
- **Language**: Dart
- **Backend**: Supabase (Authentication + Database)
- **API**: REST API for disease detection
- **State Management**: Provider pattern
- **HTTP Client**: Dio for API communication
- **Image Handling**: Image picker and caching

## 📋 Prerequisites

- Flutter SDK (3.0.0 or higher)
- Dart SDK (2.17.0 or higher)
- Android Studio / VS Code
- Android SDK (for Android builds)
- Xcode (for iOS builds, macOS only)

## 🔧 Setup Instructions

### 1. Clone and Navigate
```bash
cd mobile_app
```

### 2. Install Dependencies
```bash
flutter pub get
```

### 3. Configure Supabase
Create a `.env` file in the `mobile_app/` directory:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 4. Update Configuration
Edit `lib/main.dart` and replace the placeholder values:
```dart
await Supabase.initialize(
  url: 'YOUR_ACTUAL_SUPABASE_URL',
  anonKey: 'YOUR_ACTUAL_SUPABASE_ANON_KEY',
);
```

### 5. Run the App
```bash
flutter run
```

## 🎨 Customization

### Adding App Images
1. Place your images in `assets/images/`
2. Uncomment the splash and icon configurations in `pubspec.yaml`
3. Run the generation commands:
   ```bash
   flutter pub run flutter_native_splash:create
   flutter pub run flutter_launcher_icons
   ```

### Theme Colors
The app uses a green theme. To change colors, update the theme in `lib/main.dart`.

## 📱 Building for Production

### Android APK
```bash
flutter build apk --release
```

### Android App Bundle (Google Play)
```bash
flutter build appbundle --release
```

### iOS (macOS only)
```bash
flutter build ios --release
```

## 🔌 API Integration

The app communicates with the Crop Disease Detection API:

- **Base URL**: Configured in `lib/services/api_service.dart`
- **Endpoints**:
  - `POST /api/upload` - Upload images for detection
  - `GET /api/history` - Get detection history
  - `GET /api/detections/{id}` - Get specific detection

## 🧪 Testing

### Unit Tests
```bash
flutter test
```

### Integration Tests
```bash
flutter test integration_test/
```

## 🚀 Deployment

### Google Play Store
1. Build app bundle: `flutter build appbundle --release`
2. Upload to Google Play Console
3. Configure store listing and release

### App Store (iOS)
1. Build iOS app: `flutter build ios --release`
2. Archive in Xcode
3. Upload to App Store Connect

## 📁 Project Structure

```
lib/
├── main.dart              # App entry point
├── models/                # Data models
│   └── detection_result.dart
├── screens/               # UI screens
│   ├── auth/             # Authentication screens
│   ├── home_screen.dart  # Main dashboard
│   ├── upload_screen.dart # Image upload
│   └── result_screen.dart # Results display
├── services/              # Business logic
│   ├── auth_service.dart # Authentication
│   └── api_service.dart  # API communication
└── widgets/               # Reusable UI components
    ├── custom_button.dart
    └── custom_text_field.dart
```

## 🔍 Troubleshooting

### Common Issues:

1. **Supabase Connection Error**
   - Verify your Supabase URL and key
   - Check internet connectivity

2. **Image Upload Fails**
   - Verify API endpoint is accessible
   - Check image file size and format

3. **Build Errors**
   - Run `flutter clean` and `flutter pub get`
   - Check Flutter and Dart versions

4. **Missing Images**
   - Add required images to `assets/images/`
   - Or comment out splash/icon configs temporarily

## 📞 Support

- **API Issues**: Check the main project documentation
- **Flutter Issues**: Check Flutter documentation and community
- **Supabase Issues**: Check Supabase documentation

## 🔄 Updates

To update the app:
1. Pull latest changes: `git pull`
2. Update dependencies: `flutter pub get`
3. Test the app: `flutter run`
4. Build for production when ready

---

**Happy Coding! 🌱📱**