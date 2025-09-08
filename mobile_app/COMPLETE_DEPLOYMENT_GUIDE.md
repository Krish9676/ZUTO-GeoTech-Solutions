# Complete Mobile App Deployment Guide

## 🚀 Crop Disease Detection Mobile App - Deployment Ready

This guide covers the complete deployment process for the Crop Disease Detection mobile application.

## 📱 App Features

### ✅ Completed Features
- **AI-Powered Disease Detection**: Uses your fixed backend API with proper disease descriptions
- **Crop Selection**: Dropdown with available crops from API
- **Image Upload**: Camera and gallery support
- **Detailed Results**: Shows diagnosis, confidence, recommendations, and heatmaps
- **History Tracking**: View all previous detections
- **LLM Integration**: Displays AI-generated insights and recommendations
- **Error Handling**: Comprehensive error handling and loading states
- **Modern UI**: Material Design 3 with dark/light theme support

### 🔧 Backend Integration
- **API Endpoint**: `https://crop-disease-detection-api-0spd.onrender.com`
- **Disease Descriptions**: All rice diseases now properly mapped
- **LLaMA Integration**: Working AI recommendations
- **Heatmap Visualization**: Available for disease analysis

## 🛠️ Prerequisites

### Development Environment
1. **Flutter SDK** (3.0.0 or higher)
   ```bash
   flutter --version
   ```

2. **Android Studio** (for Android development)
3. **Xcode** (for iOS development - macOS only)
4. **VS Code** or **Android Studio** (IDE)

### Required Tools
- **Git** (for version control)
- **Node.js** (if using any JS-based tools)
- **Java JDK** (for Android builds)

## 📦 Installation & Setup

### 1. Clone and Setup
```bash
# Navigate to mobile app directory
cd mobile_app

# Install dependencies
flutter pub get

# Verify installation
flutter doctor
```

### 2. Configuration
The app is pre-configured to work with your deployed backend:
- **API URL**: `https://crop-disease-detection-api-0spd.onrender.com`
- **Timeout**: 60 seconds
- **Image Support**: JPG, JPEG, PNG
- **Max Image Size**: 5MB

### 3. Test the App
```bash
# Run on connected device/emulator
flutter run

# Or run in debug mode
flutter run --debug
```

## 🏗️ Build for Production

### Android Build

#### 1. Generate Keystore
```bash
# Create keystore for signing
keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

#### 2. Configure Signing
Create `android/key.properties`:
```properties
storePassword=<password from previous step>
keyPassword=<password from previous step>
keyAlias=upload
storeFile=<path to keystore file>
```

#### 3. Update build.gradle
The `android/app/build.gradle` should include:
```gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

#### 4. Build APK
```bash
# Build release APK
flutter build apk --release

# Build App Bundle (recommended for Play Store)
flutter build appbundle --release
```

### iOS Build (macOS only)

#### 1. Configure Xcode
1. Open `ios/Runner.xcworkspace` in Xcode
2. Set your team and bundle identifier
3. Configure signing & capabilities

#### 2. Build iOS App
```bash
# Build for iOS
flutter build ios --release

# Build IPA for App Store
flutter build ipa --release
```

## 📱 App Store Deployment

### Google Play Store (Android)

#### 1. Create Developer Account
- Visit [Google Play Console](https://play.google.com/console)
- Pay $25 one-time registration fee
- Complete developer profile

#### 2. Prepare App Listing
- **App Name**: Crop Disease Detection
- **Short Description**: AI-powered crop disease detection for farmers
- **Full Description**: 
  ```
  Detect crop diseases instantly using AI technology. Upload photos of your crops to get detailed disease analysis, treatment recommendations, and prevention tips. Supports rice, wheat, maize, tomato, potato, and more crops.
  
  Features:
  • AI-powered disease detection
  • Detailed treatment recommendations
  • Heatmap visualization
  • Detection history
  • Multiple crop support
  • Offline-capable
  ```

#### 3. Upload App Bundle
- Upload the `.aab` file from `build/app/outputs/bundle/release/`
- Complete store listing details
- Submit for review

### Apple App Store (iOS)

#### 1. Create Developer Account
- Visit [Apple Developer](https://developer.apple.com)
- Pay $99/year subscription
- Complete enrollment

#### 2. Prepare App Listing
- **App Name**: Crop Disease Detection
- **Subtitle**: AI Crop Disease Scanner
- **Description**: Similar to Android listing

#### 3. Upload via Xcode
- Archive the app in Xcode
- Upload to App Store Connect
- Complete store listing
- Submit for review

## 🔧 Configuration Files

### App Configuration
- **API Base URL**: `mobile_app_config.json`
- **Dependencies**: `pubspec.yaml`
- **Android Config**: `android/app/build.gradle`
- **iOS Config**: `ios/Runner/Info.plist`

### Environment Variables
Create `.env` file for sensitive data:
```env
API_BASE_URL=https://crop-disease-detection-api-0spd.onrender.com
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
```

## 🧪 Testing

### Unit Tests
```bash
flutter test
```

### Integration Tests
```bash
flutter test integration_test/
```

### Manual Testing Checklist
- [ ] Image upload from camera
- [ ] Image upload from gallery
- [ ] Crop selection dropdown
- [ ] Disease detection accuracy
- [ ] Result screen display
- [ ] History functionality
- [ ] Error handling
- [ ] Network connectivity
- [ ] App performance

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] All features tested
- [ ] API endpoints working
- [ ] Error handling implemented
- [ ] Performance optimized
- [ ] App icons and splash screen configured
- [ ] Privacy policy created
- [ ] Terms of service created

### Android Deployment
- [ ] Keystore generated
- [ ] App signed
- [ ] APK/AAB built
- [ ] Play Store listing prepared
- [ ] Screenshots taken
- [ ] App uploaded to Play Console

### iOS Deployment
- [ ] Apple Developer account active
- [ ] App configured in Xcode
- [ ] Provisioning profiles set up
- [ ] App built and archived
- [ ] App Store Connect listing prepared
- [ ] App uploaded to App Store Connect

## 📊 Monitoring & Analytics

### Recommended Tools
1. **Firebase Analytics** (optional)
2. **Crashlytics** (optional)
3. **App Store Analytics**
4. **Custom API monitoring**

### Key Metrics to Track
- App downloads
- Daily/monthly active users
- Disease detection accuracy
- API response times
- Crash rates
- User feedback

## 🔄 Updates & Maintenance

### Regular Updates
1. **Backend API updates**
2. **New disease models**
3. **UI/UX improvements**
4. **Bug fixes**
5. **Performance optimizations**

### Version Management
- Follow semantic versioning (1.0.0, 1.1.0, 2.0.0)
- Update version in `pubspec.yaml`
- Document changes in release notes

## 🆘 Troubleshooting

### Common Issues
1. **Build failures**: Check Flutter version and dependencies
2. **API errors**: Verify backend is running
3. **Image upload issues**: Check file size and format
4. **Signing errors**: Verify keystore configuration

### Support Resources
- [Flutter Documentation](https://flutter.dev/docs)
- [Android Developer Guide](https://developer.android.com)
- [iOS Developer Guide](https://developer.apple.com/ios)

## 📞 Support

For technical support or questions:
- Check the troubleshooting section
- Review Flutter documentation
- Test with the provided API endpoints
- Verify all configuration files

---

## 🎉 Ready for Deployment!

Your mobile app is now fully configured and ready for deployment. The backend API is working with proper disease descriptions and LLaMA integration, and the mobile app has all the necessary features for a production-ready crop disease detection application.

**Next Steps:**
1. Test the app thoroughly
2. Build release versions
3. Submit to app stores
4. Monitor and maintain

Good luck with your deployment! 🚀
