# 📱 Mobile App Deployment Checklist

## 🎯 **Pre-Deployment Requirements**

### **✅ Development Environment Setup**
- [ ] Flutter SDK installed and configured
- [ ] Android Studio with Android SDK
- [ ] Xcode installed (for iOS, Mac only)
- [ ] Git repository set up
- [ ] API endpoint tested and working

### **✅ App Development Completed**
- [ ] Core functionality implemented
- [ ] API integration working
- [ ] Image upload and processing
- [ ] Result display and sharing
- [ ] Error handling implemented
- [ ] Offline functionality (optional)

## 🤖 **Android Deployment (Google Play Store)**

### **Step 1: Prepare Android Build**

#### **A. Configure App Signing**
Create `android/key.properties`:
```properties
storePassword=your_store_password
keyPassword=your_key_password
keyAlias=your_key_alias
storeFile=../app/upload-keystore.jks
```

#### **B. Generate Signing Key**
```bash
# Generate upload keystore
keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload

# Move to android/app/
mv ~/upload-keystore.jks android/app/
```

#### **C. Configure build.gradle**
Update `android/app/build.gradle`:
```gradle
android {
    compileSdkVersion 34
    
    defaultConfig {
        applicationId "com.cropdetection.app"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
        multiDexEnabled true
    }
    
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
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

### **Step 2: Build Android Release**

#### **A. Build App Bundle (Recommended)**
```bash
# Clean previous builds
flutter clean
flutter pub get

# Build release app bundle
flutter build appbundle --release

# Output: build/app/outputs/bundle/release/app-release.aab
```

#### **B. Build APK (Alternative)**
```bash
# Build release APK
flutter build apk --release

# Output: build/app/outputs/flutter-apk/app-release.apk
```

### **Step 3: Google Play Console Setup**

#### **A. Create Developer Account**
- [ ] Sign up at https://play.google.com/console
- [ ] Pay $25 registration fee
- [ ] Complete developer profile

#### **B. Create New App**
- [ ] App name: "Crop Disease Detection AI"
- [ ] Default language: English
- [ ] App or game: App
- [ ] Free or paid: Free

#### **C. App Content**
- [ ] **Privacy Policy**: Create and host privacy policy
- [ ] **App Category**: Productivity or Education
- [ ] **Content Rating**: Complete questionnaire
- [ ] **Target Audience**: Adults
- [ ] **Data Safety**: Complete data collection disclosure

### **Step 4: Store Listing**

#### **A. App Details**
```
App Name: Crop Disease Detection AI
Short Description: AI-powered crop disease detection for farmers
Full Description:
Detect crop diseases instantly with AI! Upload photos of your crops and get:
• Accurate disease identification
• Confidence scores
• Treatment recommendations
• Support for 21+ crop types
• Offline viewing of results

Supported crops: Banana, Brinjal, Cabbage, Cauliflower, Chilli, Cotton, Grapes, Maize, Mango, Mustard, Onion, Oranges, Papaya, Pomegranate, Potato, Rice, Soybean, Sugarcane, Tobacco, Tomato, Wheat

Perfect for farmers, agricultural students, and crop consultants.
```

#### **B. Graphics Assets**
- [ ] **App Icon**: 512x512 PNG
- [ ] **Feature Graphic**: 1024x500 PNG
- [ ] **Screenshots**: At least 2, up to 8 (phone + tablet)
- [ ] **Video** (optional): YouTube demo video

#### **C. Screenshots Requirements**
```bash
# Generate screenshots
flutter drive --target=test_driver/screenshot_test.dart

# Required sizes:
# Phone: 320dp to 3840dp (16:9 to 2:1 ratio)
# Tablet: 320dp to 3840dp (16:9 to 2:1 ratio)
```

### **Step 5: Upload and Review**

#### **A. Upload App Bundle**
- [ ] Go to Release → Production
- [ ] Upload app-release.aab
- [ ] Complete release notes
- [ ] Set rollout percentage (start with 20%)

#### **B. Review Checklist**
- [ ] All store listing fields completed
- [ ] Privacy policy accessible
- [ ] App content ratings completed
- [ ] Data safety form completed
- [ ] App bundle uploaded successfully

## 🍎 **iOS Deployment (Apple App Store)**

### **Step 1: Apple Developer Account**

#### **A. Enrollment**
- [ ] Sign up at https://developer.apple.com
- [ ] Pay $99/year enrollment fee
- [ ] Complete identity verification

#### **B. Certificates and Profiles**
```bash
# Open Xcode
open ios/Runner.xcworkspace

# Configure signing in Xcode:
# 1. Select Runner target
# 2. Go to Signing & Capabilities
# 3. Select your team
# 4. Enable "Automatically manage signing"
```

### **Step 2: Configure iOS Build**

#### **A. Update Info.plist**
Update `ios/Runner/Info.plist`:
```xml
<key>CFBundleDisplayName</key>
<string>Crop Disease Detection</string>
<key>CFBundleIdentifier</key>
<string>com.cropdetection.app</string>
<key>CFBundleVersion</key>
<string>1</string>
<key>CFBundleShortVersionString</key>
<string>1.0.0</string>

<!-- Camera permission -->
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to capture crop images for disease detection.</string>

<!-- Photo library permission -->
<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to select crop images for analysis.</string>
```

#### **B. App Icons**
```bash
# Generate iOS app icons
flutter pub run flutter_launcher_icons

# Manually add icons to ios/Runner/Assets.xcassets/AppIcon.appiconset/
# Required sizes: 20x20, 29x29, 40x40, 58x58, 60x60, 80x80, 87x87, 120x120, 180x180, 1024x1024
```

### **Step 3: Build iOS Release**

#### **A. Build for Release**
```bash
# Clean and build
flutter clean
flutter pub get

# Build iOS release
flutter build ios --release
```

#### **B. Archive in Xcode**
```bash
# Open workspace in Xcode
open ios/Runner.xcworkspace

# In Xcode:
# 1. Select "Any iOS Device" as target
# 2. Product → Archive
# 3. Wait for archive to complete
# 4. Click "Distribute App"
# 5. Select "App Store Connect"
# 6. Upload to App Store Connect
```

### **Step 4: App Store Connect**

#### **A. Create App Record**
- [ ] Go to https://appstoreconnect.apple.com
- [ ] Click "My Apps" → "+" → "New App"
- [ ] Fill in app information:
  - **Name**: Crop Disease Detection AI
  - **Bundle ID**: com.cropdetection.app
  - **SKU**: crop-disease-detection-001
  - **Primary Language**: English

#### **B. App Information**
```
Name: Crop Disease Detection AI
Subtitle: AI-Powered Crop Health Analysis
Category: Productivity
Secondary Category: Education

Description:
Transform your farming with AI-powered crop disease detection! Simply upload a photo of your crop, and our advanced AI will:

🔍 Identify diseases with high accuracy
📊 Provide confidence scores
💡 Suggest treatment recommendations
🌾 Support 21+ crop types
📱 Work offline for viewing results

Supported Crops:
Banana, Brinjal, Cabbage, Cauliflower, Chilli, Cotton, Grapes, Maize, Mango, Mustard, Onion, Oranges, Papaya, Pomegranate, Potato, Rice, Soybean, Sugarcane, Tobacco, Tomato, Wheat

Perfect for:
• Farmers and agricultural workers
• Agricultural students and researchers
• Crop consultants and advisors
• Anyone interested in crop health

Keywords: agriculture, farming, crop, disease, AI, detection, plant, health, diagnosis
```

#### **C. App Store Assets**
- [ ] **App Icon**: 1024x1024 PNG
- [ ] **Screenshots**: 
  - iPhone: 6.7", 6.5", 5.5" displays
  - iPad: 12.9", 11" displays
- [ ] **App Preview** (optional): 15-30 second video

### **Step 5: Submit for Review**

#### **A. Build Selection**
- [ ] Select uploaded build
- [ ] Add "What's New in This Version"
- [ ] Complete App Review Information
- [ ] Add review notes if needed

#### **B. Release Options**
- [ ] **Manual Release**: Control when app goes live
- [ ] **Automatic Release**: Goes live after approval
- [ ] **Scheduled Release**: Set specific date/time

## 🔒 **Security & Privacy**

### **Privacy Policy Requirements**

#### **A. Create Privacy Policy**
```markdown
# Privacy Policy for Crop Disease Detection AI

## Information We Collect
- Crop images uploaded for analysis
- Device information for app functionality
- Usage analytics (anonymous)

## How We Use Information
- Process images for disease detection
- Improve AI model accuracy
- Provide customer support

## Data Storage
- Images stored securely on Supabase
- Data encrypted in transit and at rest
- No personal information collected

## Third-Party Services
- Supabase (database and storage)
- Render (API hosting)
- Analytics services (anonymous)

## Contact
Email: support@cropdetection.com
Website: https://cropdetection.com
```

#### **B. Host Privacy Policy**
- [ ] Create website or use GitHub Pages
- [ ] Make privacy policy accessible
- [ ] Add link to app stores

### **Data Safety (Android)**
- [ ] **Data Collection**: Images, device info
- [ ] **Data Sharing**: None
- [ ] **Data Security**: Encrypted
- [ ] **Data Deletion**: User can request deletion

## 📊 **Analytics & Monitoring**

### **Firebase Setup**

#### **A. Add Firebase to Flutter**
```yaml
# pubspec.yaml
dependencies:
  firebase_core: ^2.15.1
  firebase_analytics: ^10.4.5
  firebase_crashlytics: ^3.3.5
```

#### **B. Configure Firebase**
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login and configure
firebase login
flutter pub global activate flutterfire_cli
flutterfire configure
```

### **App Performance Monitoring**
- [ ] Crash reporting (Crashlytics)
- [ ] Performance monitoring
- [ ] User analytics
- [ ] API usage tracking

## 🚀 **Launch Strategy**

### **Soft Launch (Week 1)**
- [ ] Release to limited regions
- [ ] Monitor for critical issues
- [ ] Gather initial user feedback
- [ ] Fix any urgent bugs

### **Full Launch (Week 2)**
- [ ] Global release
- [ ] Social media announcement
- [ ] Press release
- [ ] Agricultural community outreach

### **Post-Launch (Ongoing)**
- [ ] Monitor app store reviews
- [ ] Respond to user feedback
- [ ] Plan feature updates
- [ ] Track key metrics

## 📈 **Success Metrics**

### **Technical KPIs**
- [ ] App crash rate < 1%
- [ ] App store rating > 4.0
- [ ] API response time < 5s
- [ ] Image upload success rate > 95%

### **Business KPIs**
- [ ] Daily active users
- [ ] Monthly downloads
- [ ] User retention rate
- [ ] Feature usage analytics

## 🛠️ **Maintenance & Updates**

### **Regular Updates**
- [ ] Bug fixes and improvements
- [ ] New crop support
- [ ] UI/UX enhancements
- [ ] Performance optimizations

### **Version Management**
```bash
# Update version in pubspec.yaml
version: 1.0.1+2

# Build and deploy new version
flutter build appbundle --release
flutter build ios --release
```

---

## ✅ **Final Deployment Checklist**

### **Pre-Submission**
- [ ] App functionality tested thoroughly
- [ ] API integration working
- [ ] Privacy policy created and hosted
- [ ] App store assets prepared
- [ ] Developer accounts set up

### **Android Submission**
- [ ] App bundle built and signed
- [ ] Google Play Console configured
- [ ] Store listing completed
- [ ] App uploaded and submitted

### **iOS Submission**
- [ ] iOS build archived in Xcode
- [ ] App Store Connect configured
- [ ] App information completed
- [ ] Build submitted for review

### **Post-Submission**
- [ ] Monitor review status
- [ ] Respond to reviewer feedback
- [ ] Plan launch marketing
- [ ] Set up user support channels

---

**🎉 Your crop disease detection app is ready to help farmers worldwide! 🌱📱**

**Next Steps**: Submit to app stores and start helping farmers improve their crop health!