/**
 * Crop Disease Detection API Integration
 * 
 * This file contains the core JavaScript code to integrate with your deployed API:
 * https://crop-disease-detection-api-0spd.onrender.com/
 */

class CropDiseaseAPI {
    constructor(baseURL = 'https://crop-disease-detection-api-0spd.onrender.com') {
        this.baseURL = baseURL;
        this.apiURL = `${baseURL}/api`;
    }

    /**
     * Check if the API is running
     */
    async checkStatus() {
        try {
            const response = await fetch(`${this.baseURL}/`);
            const data = await response.json();
            return {
                success: true,
                status: data.status,
                message: data.message
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Upload and analyze an image for pest/disease detection
     * @param {File} imageFile - The image file to analyze
     * @param {string} cropName - Optional crop name
     * @returns {Promise<Object>} Analysis results
     */
    async analyzeImage(imageFile, cropName = null) {
        try {
            const formData = new FormData();
            formData.append('file', imageFile);
            
            if (cropName) {
                formData.append('crop_name', cropName);
            }

            const response = await fetch(`${this.apiURL}/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            return {
                success: true,
                data: result
            };

        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Get detection history
     * @returns {Promise<Object>} List of previous detections
     */
    async getHistory() {
        try {
            const response = await fetch(`${this.apiURL}/history`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const history = await response.json();
            return {
                success: true,
                data: history
            };

        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Get a specific detection by ID
     * @param {string} detectionId - The detection ID
     * @returns {Promise<Object>} Detection details
     */
    async getDetection(detectionId) {
        try {
            const response = await fetch(`${this.apiURL}/detections/${detectionId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const detection = await response.json();
            return {
                success: true,
                data: detection
            };

        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
}

// Example usage:
async function exampleUsage() {
    const api = new CropDiseaseAPI();
    
    // 1. Check API status
    const status = await api.checkStatus();
    if (status.success) {
        console.log('✅ API is running:', status.message);
    } else {
        console.log('❌ API Error:', status.error);
        return;
    }

    // 2. Example of analyzing an image (when you have a file)
    // const result = await api.analyzeImage(imageFile, 'rice');
    // if (result.success) {
    //     console.log('Analysis results:', result.data);
    // }

    // 3. Get detection history
    const history = await api.getHistory();
    if (history.success) {
        console.log(`Found ${history.data.length} previous detections`);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CropDiseaseAPI;
}

// Make available globally in browser
if (typeof window !== 'undefined') {
    window.CropDiseaseAPI = CropDiseaseAPI;
    window.exampleUsage = exampleUsage;
}
