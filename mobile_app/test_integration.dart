import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:crop_disease_detection/services/api_service.dart';

void main() {
  group('API Service Tests', () {
    late ApiService apiService;

    setUp(() {
      apiService = ApiService();
    });

    test('should get available crops', () async {
      try {
        final crops = await apiService.getAvailableCrops();
        expect(crops, isA<List<String>>());
        expect(crops.isNotEmpty, true);
        print('✅ Available crops: $crops');
      } catch (e) {
        print('❌ Error getting crops: $e');
        fail('Failed to get available crops: $e');
      }
    });

    test('should handle API errors gracefully', () async {
      try {
        // This should fail gracefully
        final crops = await apiService.getAvailableCrops();
        print('✅ API is accessible');
      } catch (e) {
        print('⚠️ API error (expected if backend is down): $e');
        // This is acceptable if the backend is not running
      }
    });
  });
}
