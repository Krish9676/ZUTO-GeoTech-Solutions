#!/usr/bin/env python3

import os
import sys
import argparse
import json
import random
import datetime
import uuid
from pathlib import Path

# Sample data generation for crop disease detection

def generate_random_url(base_url, bucket, filename):
    """Generate a random URL for an image"""
    return f"{base_url}/{bucket}/{filename}"

def generate_random_diagnosis(pest_name, confidence):
    """Generate a random diagnosis for a pest/disease"""
    diagnoses = {
        "Fall Armyworm": [
            "The Fall Armyworm (Spodoptera frugiperda) is a significant pest affecting maize crops. The larvae feed on leaves, creating a windowing effect and leaving behind frass (excrement). In severe cases, they can destroy the growing point, leading to plant death. Control measures include early detection, biological controls like natural predators, and targeted insecticides when necessary. Crop rotation and early planting can help reduce infestations.",
            "Your maize crop is showing signs of Fall Armyworm infestation. These caterpillars feed aggressively on leaves and can bore into the whorl. The damage appears as ragged feeding and visible frass. For management, consider applying Bacillus thuringiensis (Bt) based products for young larvae or approved insecticides for severe infestations. Monitoring and early intervention are crucial for effective control."
        ],
        "Corn Leaf Blight": [
            "Northern Corn Leaf Blight is a fungal disease caused by Exserohilum turcicum. It appears as long, elliptical gray-green or tan lesions on corn leaves. The disease thrives in humid conditions with moderate temperatures. Management strategies include planting resistant varieties, crop rotation, fungicide application, and proper field sanitation by removing crop debris.",
            "Your corn is affected by Corn Leaf Blight, characterized by the cigar-shaped lesions on the leaves. This fungal disease can reduce photosynthetic area and yield if severe. To manage this condition, consider applying a foliar fungicide, especially if the disease appears before tasseling. For future plantings, select resistant hybrids and implement crop rotation to reduce disease pressure."
        ],
        "Common Rust": [
            "Common rust in maize is caused by the fungus Puccinia sorghi. It appears as small, circular to elongate, cinnamon-brown pustules on both leaf surfaces. Severe infections can cause leaf death and significant yield loss. Control measures include planting resistant varieties, early application of fungicides, and avoiding excessive nitrogen fertilization which can increase susceptibility.",
            "The image shows Common Rust infection on your maize crop. This fungal disease produces distinctive reddish-brown pustules scattered across the leaf surface. While moderate infections may not significantly impact yield, severe cases can reduce photosynthesis and grain fill. Consider applying a triazole or strobilurin fungicide if the disease is progressing rapidly, especially before tasseling stage."
        ],
        "Gray Leaf Spot": [
            "Gray Leaf Spot is caused by the fungus Cercospora zeae-maydis. It appears as rectangular lesions that are tan to gray and run parallel to the leaf veins. The disease is favored by warm, humid conditions and continuous corn cultivation. Management includes crop rotation, tillage to reduce residue, planting resistant hybrids, and timely fungicide applications.",
            "Your corn is showing symptoms of Gray Leaf Spot, a significant fungal disease that can cause substantial yield loss. The rectangular gray lesions running parallel to the leaf veins are characteristic of this infection. The disease is progressing up the plant, which can impact grain fill if it reaches the upper leaves. Consider applying a fungicide with mixed modes of action, and for future seasons, implement crop rotation and select resistant hybrids."
        ],
        "Northern Leaf Blight": [
            "Northern Leaf Blight in corn is caused by Exserohilum turcicum. It produces distinctive cigar-shaped lesions that are grayish-green to tan. The disease can cause significant yield loss if it develops before or during tasseling. Management strategies include planting resistant hybrids, crop rotation, fungicide applications, and residue management.",
            "The image shows Northern Leaf Blight affecting your corn crop. The long, elliptical lesions are typical of this fungal disease. Under favorable conditions (moderate temperatures and high humidity), this disease can spread rapidly. For immediate management, apply a foliar fungicide containing a strobilurin and triazole mixture. Long-term strategies should include crop rotation and selecting hybrids with resistance to this pathogen."
        ],
        "Healthy": [
            "Your crop appears healthy with no visible signs of disease or pest damage. The leaves show good coloration and structure, indicating proper nutrition and growing conditions. Continue with your current management practices, including regular monitoring for early detection of any potential issues.",
            "The plant in the image is healthy. The leaves display normal color, structure, and development with no visible symptoms of disease, pest damage, or nutrient deficiencies. Maintain your current agricultural practices, including appropriate irrigation and fertilization schedules, while continuing regular scouting for any emerging issues."
        ],
        "Bacterial Leaf Blight": [
            "Bacterial Leaf Blight, caused by Xanthomonas oryzae pv. oryzae, is a serious disease of rice. It appears as water-soaked lesions that turn yellow-orange and eventually gray-white with wavy edges. The disease is favored by high humidity and temperatures. Management includes planting resistant varieties, balanced fertilization (avoiding excess nitrogen), proper spacing, and copper-based bactericides in severe cases.",
            "Your rice crop is showing Bacterial Leaf Blight infection. The characteristic lesions start at the leaf margins and progress inward, turning from yellow to white as they mature. This bacterial disease can cause significant yield losses, especially in susceptible varieties. For management, drain the field temporarily if possible, avoid excessive nitrogen application, and consider copper-based products as a protective measure for uninfected plants."
        ],
        "Leaf Blast": [
            "Rice Blast, caused by Magnaporthe oryzae, is one of the most destructive rice diseases worldwide. It appears as diamond-shaped lesions with gray centers and brown borders on leaves. The disease thrives in conditions of high humidity and moderate temperatures. Control measures include resistant varieties, balanced fertilization, proper water management, and fungicide applications at critical growth stages.",
            "The image shows Rice Leaf Blast infection. The characteristic diamond or spindle-shaped lesions with gray centers and dark borders are visible on the leaves. This fungal disease can significantly reduce photosynthetic area and yield. For immediate management, apply a systemic fungicide containing tricyclazole or azoxystrobin. Long-term strategies should include resistant varieties and avoiding dense canopies through proper spacing and nitrogen management."
        ],
        "Powdery Mildew": [
            "Powdery Mildew in wheat is caused by Blumeria graminis f. sp. tritici. It appears as white, powdery patches on leaves, stems, and heads. The disease is favored by moderate temperatures and high humidity but can develop without free water. Management includes resistant varieties, balanced fertilization, proper spacing, and timely fungicide applications, particularly with triazoles or strobilurins.",
            "Your wheat crop is affected by Powdery Mildew, as evidenced by the white, powdery fungal growth on the leaf surface. This disease can reduce photosynthesis and yield if it spreads to the flag leaf and head. For control, apply a fungicide containing a triazole (like tebuconazole) or a strobilurin (like azoxystrobin). The disease is favored by dense canopies, so consider reducing nitrogen rates in future plantings if this is a recurring problem."
        ],
        "Early Blight": [
            "Early Blight in tomatoes and potatoes is caused by Alternaria solani. It appears as dark brown to black lesions with concentric rings, often surrounded by a yellow halo. The disease typically starts on lower leaves and moves upward. Management includes crop rotation, proper spacing, staking or trellising tomatoes, avoiding overhead irrigation, removing infected leaves, and fungicide applications.",
            "The image shows Early Blight infection on your tomato plant. The characteristic dark lesions with concentric rings (target-like pattern) are visible on the lower leaves. This fungal disease typically progresses from the bottom of the plant upward. Remove infected leaves, improve air circulation around plants, and apply a fungicide containing chlorothalonil or copper. Mulching can help prevent spore splash from soil to leaves."
        ],
        "Late Blight": [
            "Late Blight, caused by Phytophthora infestans, is a devastating disease of potatoes and tomatoes. It appears as water-soaked, gray-green lesions that quickly turn brown-black. White fungal growth may be visible on the undersides of leaves in humid conditions. The disease can spread rapidly in cool, wet weather. Management includes resistant varieties, preventive fungicides, proper spacing, avoiding overhead irrigation, and destroying infected plants.",
            "Your potato crop is showing symptoms of Late Blight, a highly destructive disease that can cause rapid plant death. The dark, water-soaked lesions with fuzzy white growth (in humid conditions) are characteristic. This disease can spread extremely quickly in cool, wet weather. Immediately apply a fungicide containing mefenoxam, chlorothalonil, or copper. Remove severely infected plants and dispose of them away from the garden to reduce inoculum."
        ]
    }
    
    # Default diagnosis if pest name not in the dictionary
    default_diagnosis = f"The image shows signs of {pest_name} affecting your crop. Based on the {confidence:.1f}% confidence of our detection model, we recommend consulting with a local agricultural extension officer for specific treatment options tailored to your region and growing conditions. Regular monitoring and early intervention are key to managing this issue effectively."
    
    # Get diagnoses for the pest name or use default
    pest_diagnoses = diagnoses.get(pest_name, [default_diagnosis])
    
    # Return a random diagnosis from the list
    return random.choice(pest_diagnoses)

def generate_sample_detection(base_url, crop_types, pest_names):
    """Generate a sample detection record"""
    # Generate a random UUID
    detection_id = str(uuid.uuid4())
    
    # Select a random crop type and pest name
    crop_name = random.choice(crop_types)
    pest_name = random.choice(pest_names)
    
    # Generate random confidence (70-100%)
    confidence = round(random.uniform(70.0, 99.9), 1)
    
    # Generate random timestamps within the last 30 days
    days_ago = random.randint(0, 30)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)
    created_at = (datetime.datetime.now() - 
                 datetime.timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago))
    created_at_str = created_at.isoformat()
    
    # Generate random image URLs
    image_filename = f"{detection_id}_{crop_name.lower().replace(' ', '_')}.jpg"
    heatmap_filename = f"{detection_id}_heatmap.jpg"
    image_url = generate_random_url(base_url, "crop-images", image_filename)
    heatmap_url = generate_random_url(base_url, "heatmaps", heatmap_filename)
    
    # Generate a diagnosis
    diagnosis = generate_random_diagnosis(pest_name, confidence)
    
    # Create the detection record
    detection = {
        "id": detection_id,
        "image_url": image_url,
        "heatmap_url": heatmap_url,
        "pest_name": pest_name,
        "confidence": confidence,
        "crop_name": crop_name,
        "diagnosis": diagnosis,
        "created_at": created_at_str,
        "updated_at": created_at_str
    }
    
    return detection

def generate_sample_data(count, output_file, base_url):
    """Generate sample detection data"""
    # Sample crop types
    crop_types = [
        "Maize", "Rice", "Wheat", "Tomato", "Potato", "Cotton"
    ]
    
    # Sample pest/disease names
    pest_names = [
        "Healthy",
        "Fall Armyworm",
        "Corn Leaf Blight",
        "Common Rust",
        "Gray Leaf Spot",
        "Northern Leaf Blight",
        "Bacterial Leaf Blight",
        "Leaf Blast",
        "Powdery Mildew",
        "Early Blight",
        "Late Blight"
    ]
    
    # Generate sample detections
    detections = []
    for _ in range(count):
        detection = generate_sample_detection(base_url, crop_types, pest_names)
        detections.append(detection)
    
    # Sort by created_at (newest first)
    detections.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Write to file
    try:
        with open(output_file, 'w') as f:
            json.dump({"detections": detections}, f, indent=2)
        return True
    except Exception as e:
        print(f"Error writing to file: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate sample detection data')
    parser.add_argument('--count', type=int, default=20,
                        help='Number of sample detections to generate')
    parser.add_argument('--output', type=str, default='sample_data.json',
                        help='Output file path')
    parser.add_argument('--base-url', type=str, default='https://example-storage.supabase.co',
                        help='Base URL for storage')
    
    args = parser.parse_args()
    
    print(f"Generating {args.count} sample detections...")
    if generate_sample_data(args.count, args.output, args.base_url):
        print(f"\n✅ Sample data generated successfully!")
        print(f"Output file: {args.output}")
    else:
        print("\n❌ Error generating sample data")
        sys.exit(1)

if __name__ == '__main__':
    main()