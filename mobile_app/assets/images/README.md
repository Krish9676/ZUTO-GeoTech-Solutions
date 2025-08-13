# Mobile App Images

This directory should contain the following images for the mobile app:

## Required Images:

1. **splash_logo.png** - Logo for the splash screen (recommended: 512x512px)
2. **app_icon.png** - Main app icon (recommended: 1024x1024px)
3. **app_icon_foreground.png** - Foreground icon for adaptive icons (recommended: 1024x1024px)

## Image Specifications:

- **Format**: PNG with transparency
- **Splash Logo**: Should be centered and work well on both light and dark backgrounds
- **App Icon**: Should be simple, recognizable, and work well at small sizes
- **Colors**: Use the app's green theme (#4CAF50) for consistency

## Current Status:
⚠️ **Images are missing!** You need to add these images before building the app.

## Quick Fix:
1. Create or obtain the required images
2. Place them in this directory
3. Run `flutter pub get` to update dependencies
4. Generate splash screen: `flutter pub run flutter_native_splash:create`
5. Generate app icons: `flutter pub run flutter_launcher_icons`

## Alternative:
If you don't have custom images yet, you can temporarily comment out the splash and icon configurations in `pubspec.yaml` to build the app without them.
