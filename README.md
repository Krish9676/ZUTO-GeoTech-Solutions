# Crop Disease Detection Project

A comprehensive solution for detecting crop diseases using machine learning, consisting of a REST API and a Flutter mobile application.

## 🏗️ Project Structure

This project is organized into two main components:

```
PD_application/
├── api/                    # 🚀 REST API for disease detection
│   ├── app/               # Core API logic
│   ├── models/            # ML model files
│   ├── tests/             # API tests
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile         # Container configuration
│   └── README.md          # API documentation
├── mobile_app/            # 📱 Flutter mobile application
│   ├── lib/               # Dart source code
│   ├── assets/            # Images and resources
│   └── pubspec.yaml       # Flutter dependencies
├── docs/                  # 📚 Project documentation
├── scripts/               # 🛠️ Utility scripts
└── README.md              # This file
```

## 🚀 Quick Start

### Option 1: Start with the API
1. **Navigate to API directory:**
   ```bash
   cd api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

4. **Run the API:**
   ```bash
   python run.py --reload
   ```

### Option 2: Start with the Mobile App
1. **Navigate to mobile app directory:**
   ```bash
   cd mobile_app
   ```

2. **Install Flutter dependencies:**
   ```bash
   flutter pub get
   ```

3. **Run the app:**
   ```bash
   flutter run
   ```

## 🔧 Development Workflow

### Recommended Development Order:
1. **Start with API development** - Get the backend working first
2. **Test API endpoints** - Ensure all functionality works
3. **Develop mobile app** - Build the Flutter interface
4. **Integration testing** - Connect mobile app to API
5. **Deployment** - Deploy both components

### Why This Structure?
- **Clear separation of concerns** - API and mobile app are independent
- **Easier testing** - Test API without mobile app distractions
- **Better version control** - Separate commit histories
- **Cleaner dependencies** - No mixing of Python and Flutter requirements
- **Easier deployment** - Deploy API first, then integrate mobile app

## 📱 Mobile App Integration

The mobile app communicates with the API through HTTP requests. Key endpoints:

- `POST /api/upload` - Upload images for disease detection
- `GET /api/history` - Retrieve detection history
- `GET /api/detections/{id}` - Get specific detection details

## 🚀 Deployment

### API Deployment
- **Render**: Use `api/render.yaml`
- **Docker**: Use `api/Dockerfile`
- **Other platforms**: Follow `api/README.md`

### Mobile App Deployment
- **Android**: Build APK or use Google Play Console
- **iOS**: Use Xcode and App Store Connect
- **Web**: Flutter web build

## 📚 Documentation

- **API Documentation**: See `api/README.md`
- **Mobile App Guide**: See `mobile_app/README.md`
- **Deployment Guides**: See `docs/` directory
- **Integration Guide**: See `MOBILE_APP_INTEGRATION_GUIDE.md`

## 🧪 Testing

### API Testing
```bash
cd api
python -m pytest tests/
```

### Mobile App Testing
```bash
cd mobile_app
flutter test
```

## 🔍 Troubleshooting

### Common Issues:
1. **Import errors**: Ensure you're in the correct directory
2. **Model not found**: Check `api/models/` directory
3. **Environment variables**: Verify `.env` file in `api/` directory
4. **Flutter dependencies**: Run `flutter pub get` in `mobile_app/`

## 📞 Support

- **API Issues**: Check `api/README.md` and `docs/`
- **Mobile App Issues**: Check `mobile_app/README.md`
- **General Questions**: Review project documentation

## 🤝 Contributing

1. Work on API features in the `api/` directory
2. Work on mobile app features in the `mobile_app/` directory
3. Update relevant documentation
4. Test your changes thoroughly

---

**Happy Coding! 🌱🔬📱**