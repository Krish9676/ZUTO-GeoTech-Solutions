"""
Disease Description Utilities

This module provides human-readable descriptions and treatment recommendations
for various crop diseases detected by the ML model.
"""

import re
from typing import Dict, Tuple, Optional

# Disease descriptions and treatment recommendations
DISEASE_INFO = {
    # Rice diseases
    "healthy_rice": {
        "description": "Healthy rice plant with no visible disease symptoms",
        "status": "healthy",
        "recommendation": "Continue current care practices. Monitor for any changes."
    },
    "rice_bacterial_blight": {
        "description": "Bacterial blight causing white to grayish lesions on leaves",
        "status": "diseased",
        "recommendation": "Remove infected plants. Apply copper-based bactericides. Improve field drainage."
    },
    "rice_brown_spot": {
        "description": "Fungal disease causing brown, oval lesions on leaves and grains",
        "status": "diseased",
        "recommendation": "Apply fungicides. Remove crop debris. Use resistant varieties."
    },
    "rice_leaf_smut": {
        "description": "Fungal disease causing black spore masses on leaves",
        "status": "diseased",
        "recommendation": "Apply systemic fungicides. Remove infected plants. Rotate crops."
    },
    
    # Wheat diseases
    "healthy_wheat": {
        "description": "Healthy wheat plant with no visible disease symptoms",
        "status": "healthy",
        "recommendation": "Continue current care practices. Monitor for any changes."
    },
    "wheat_brown_rust": {
        "description": "Fungal rust disease causing reddish-brown pustules on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides. Use resistant varieties. Remove volunteer wheat."
    },
    "wheat_yellow_rust": {
        "description": "Fungal rust disease causing yellow-orange pustules on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides early. Use resistant varieties. Monitor weather conditions."
    },
    "wheat_septoria_leaf_blotch": {
        "description": "Fungal disease causing brown lesions with dark borders on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides. Remove crop debris. Use proper spacing."
    },
    
    # Maize/Corn diseases
    "healthy_maize": {
        "description": "Healthy maize plant with no visible disease symptoms",
        "status": "healthy",
        "recommendation": "Continue current care practices. Monitor for any changes."
    },
    "maize_gray_leaf_spot": {
        "description": "Fungal disease causing grayish-brown rectangular lesions on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides. Use resistant varieties. Remove crop debris."
    },
    "maize_common_rust": {
        "description": "Fungal rust disease causing reddish-brown pustules on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides. Use resistant varieties. Monitor humidity levels."
    },
    "maize_northern_leaf_blight": {
        "description": "Fungal disease causing long, elliptical gray lesions on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides. Use resistant varieties. Remove infected debris."
    },
    
    # Potato diseases
    "healthy_potato": {
        "description": "Healthy potato plant with no visible disease symptoms",
        "status": "healthy",
        "recommendation": "Continue current care practices. Monitor for any changes."
    },
    "potato_early_blight": {
        "description": "Fungal disease causing dark brown lesions with concentric rings on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides. Remove infected leaves. Improve air circulation."
    },
    "potato_late_blight": {
        "description": "Devastating fungal disease causing dark lesions and white mold on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides immediately. Remove infected plants. Monitor weather."
    },
    
    # Tomato diseases
    "healthy_tomato": {
        "description": "Healthy tomato plant with no visible disease symptoms",
        "status": "healthy",
        "recommendation": "Continue current care practices. Monitor for any changes."
    },
    "tomato_bacterial_spot": {
        "description": "Bacterial disease causing small, dark lesions with yellow halos on leaves",
        "status": "diseased",
        "recommendation": "Remove infected plants. Apply copper-based bactericides. Avoid overhead watering."
    },
    "tomato_early_blight": {
        "description": "Fungal disease causing dark brown lesions with concentric rings on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides. Remove infected leaves. Improve air circulation."
    },
    "tomato_late_blight": {
        "description": "Devastating fungal disease causing dark lesions and white mold on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides immediately. Remove infected plants. Monitor humidity."
    },
    "tomato_leaf_mold": {
        "description": "Fungal disease causing yellow spots with grayish mold on leaf undersides",
        "status": "diseased",
        "recommendation": "Improve air circulation. Apply fungicides. Reduce humidity."
    },
    "tomato_septoria_leaf_spot": {
        "description": "Fungal disease causing small, circular spots with dark borders on leaves",
        "status": "diseased",
        "recommendation": "Remove infected leaves. Apply fungicides. Avoid overhead watering."
    },
    "tomato_spider_mites": {
        "description": "Tiny arachnids causing stippling and webbing on leaves",
        "status": "pest_infestation",
        "recommendation": "Apply miticides. Increase humidity. Use predatory mites if possible."
    },
    "tomato_target_spot": {
        "description": "Fungal disease causing target-like lesions with concentric rings on leaves",
        "status": "diseased",
        "recommendation": "Apply fungicides. Remove infected debris. Improve air circulation."
    },
    "tomato_yellow_leaf_curl_virus": {
        "description": "Viral disease causing yellowing and curling of leaves",
        "status": "diseased",
        "recommendation": "Remove infected plants. Control whiteflies. Use resistant varieties."
    },
    "tomato_mosaic_virus": {
        "description": "Viral disease causing mottled, distorted leaves and stunted growth",
        "status": "diseased",
        "recommendation": "Remove infected plants. Control aphids. Sanitize tools."
    },
    
    # Pepper diseases
    "healthy_pepper": {
        "description": "Healthy pepper plant with no visible disease symptoms",
        "status": "healthy",
        "recommendation": "Continue current care practices. Monitor for any changes."
    },
    "pepper_bacterial_spot": {
        "description": "Bacterial disease causing small, dark lesions with yellow halos on leaves",
        "status": "diseased",
        "recommendation": "Remove infected plants. Apply copper-based bactericides. Avoid overhead watering."
    },
    
    # Cotton diseases
    "healthy_cotton": {
        "description": "Healthy cotton plant with no visible disease symptoms",
        "status": "healthy",
        "recommendation": "Continue current care practices. Monitor for any changes."
    },
    "cotton_bacterial_blight": {
        "description": "Bacterial disease causing angular lesions and leaf spots",
        "status": "diseased",
        "recommendation": "Remove infected plants. Apply copper-based bactericides. Improve drainage."
    },
    
    # Soybean diseases
    "healthy_soybean": {
        "description": "Healthy soybean plant with no visible disease symptoms",
        "status": "healthy",
        "recommendation": "Continue current care practices. Monitor for any changes."
    },
    "soybean_bacterial_blight": {
        "description": "Bacterial disease causing angular lesions and leaf spots",
        "status": "diseased",
        "recommendation": "Remove infected plants. Apply copper-based bactericides. Use resistant varieties."
    }
}

def get_disease_info(disease_name: str) -> Dict[str, str]:
    """
    Get disease information including description, status, and recommendations
    
    Args:
        disease_name: The disease class name (e.g., 'tomato_early_blight')
        
    Returns:
        Dictionary containing disease information
    """
    # Clean the disease name
    clean_name = disease_name.lower().strip()
    
    # Check if we have information for this disease
    if clean_name in DISEASE_INFO:
        return DISEASE_INFO[clean_name]
    
    # Try to match partial names
    for key, info in DISEASE_INFO.items():
        if clean_name in key or key in clean_name:
            return info
    
    # Return default information for unknown diseases
    return {
        "description": f"Unknown disease: {disease_name}",
        "status": "unknown",
        "recommendation": "Consult with agricultural experts for proper diagnosis and treatment."
    }

def format_disease_name(disease_name: str) -> str:
    """
    Convert disease class name to human-readable format
    
    Args:
        disease_name: The disease class name (e.g., 'tomato_early_blight')
        
    Returns:
        Formatted disease name (e.g., 'Tomato Early Blight')
    """
    if not disease_name:
        return "Unknown Disease"
    
    # Handle special cases
    if disease_name == "healthy_rice":
        return "Healthy Rice Plant"
    elif disease_name == "healthy_wheat":
        return "Healthy Wheat Plant"
    elif disease_name == "healthy_maize":
        return "Healthy Maize Plant"
    elif disease_name == "healthy_potato":
        return "Healthy Potato Plant"
    elif disease_name == "healthy_tomato":
        return "Healthy Tomato Plant"
    elif disease_name == "healthy_pepper":
        return "Healthy Pepper Plant"
    elif disease_name == "healthy_cotton":
        return "Healthy Cotton Plant"
    elif disease_name == "healthy_soybean":
        return "Healthy Soybean Plant"
    
    # Convert snake_case to Title Case
    # Replace underscores with spaces and capitalize each word
    formatted = disease_name.replace('_', ' ').title()
    
    # Handle common abbreviations
    formatted = formatted.replace('Rice', 'Rice')
    formatted = formatted.replace('Wheat', 'Wheat')
    formatted = formatted.replace('Maize', 'Maize')
    formatted = formatted.replace('Potato', 'Potato')
    formatted = formatted.replace('Tomato', 'Tomato')
    formatted = formatted.replace('Pepper', 'Pepper')
    formatted = formatted.replace('Cotton', 'Cotton')
    formatted = formatted.replace('Soybean', 'Soybean')
    
    return formatted

def get_severity_level(confidence: float) -> str:
    """
    Determine severity level based on confidence score
    
    Args:
        confidence: Confidence score between 0 and 1
        
    Returns:
        Severity level string
    """
    if confidence >= 0.9:
        return "Very High"
    elif confidence >= 0.8:
        return "High"
    elif confidence >= 0.7:
        return "Medium-High"
    elif confidence >= 0.6:
        return "Medium"
    elif confidence >= 0.5:
        return "Medium-Low"
    elif confidence >= 0.3:
        return "Low"
    else:
        return "Very Low"

def generate_diagnosis_summary(disease_name: str, confidence: float, crop_name: str = None) -> str:
    """
    Generate a comprehensive diagnosis summary
    
    Args:
        disease_name: The detected disease class
        confidence: Confidence score between 0 and 1
        crop_name: Optional crop name for context
        
    Returns:
        Formatted diagnosis summary
    """
    disease_info = get_disease_info(disease_name)
    formatted_name = format_disease_name(disease_name)
    severity = get_severity_level(confidence)
    confidence_pct = confidence * 100
    
    summary = f"**Diagnosis: {formatted_name}**\n\n"
    summary += f"**Confidence:** {confidence_pct:.1f}% ({severity} confidence)\n\n"
    summary += f"**Description:** {disease_info['description']}\n\n"
    summary += f"**Status:** {disease_info['status'].title()}\n\n"
    summary += f"**Recommendation:** {disease_info['recommendation']}"
    
    if crop_name:
        summary += f"\n\n**Crop:** {crop_name.title()}"
    
    return summary
