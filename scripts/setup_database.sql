-- Supabase SQL Schema for Crop Disease Detection Application

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create detections table
CREATE TABLE IF NOT EXISTS detections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_url TEXT NOT NULL,
    heatmap_url TEXT,
    pest_name TEXT NOT NULL,
    confidence DECIMAL(5, 2) NOT NULL,
    crop_name TEXT,
    diagnosis TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create RLS policies for detections table
ALTER TABLE detections ENABLE ROW LEVEL SECURITY;

-- Create policy to allow authenticated users to select their own detections
CREATE POLICY "Users can view their own detections"
    ON detections
    FOR SELECT
    USING (auth.uid() = created_by);

-- Create policy to allow authenticated users to insert detections
CREATE POLICY "Users can insert their own detections"
    ON detections
    FOR INSERT
    WITH CHECK (auth.uid() = created_by);

-- Add created_by column to track which user created the detection
ALTER TABLE detections ADD COLUMN created_by UUID REFERENCES auth.users(id);

-- Create function to automatically set updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at timestamp
CREATE TRIGGER update_detections_updated_at
BEFORE UPDATE ON detections
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- Create index on created_by for faster queries
CREATE INDEX idx_detections_created_by ON detections(created_by);

-- Create index on pest_name for faster searches
CREATE INDEX idx_detections_pest_name ON detections(pest_name);

-- Create index on crop_name for faster searches
CREATE INDEX idx_detections_crop_name ON detections(crop_name);

-- Create view for recent detections
CREATE OR REPLACE VIEW recent_detections AS
SELECT id, image_url, pest_name, confidence, crop_name, created_at
FROM detections
ORDER BY created_at DESC
LIMIT 100;

-- Create function to get detections by crop name
CREATE OR REPLACE FUNCTION get_detections_by_crop(crop TEXT)
RETURNS SETOF detections AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM detections
    WHERE crop_name ILIKE '%' || crop || '%'
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Create function to get detections by pest name
CREATE OR REPLACE FUNCTION get_detections_by_pest(pest TEXT)
RETURNS SETOF detections AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM detections
    WHERE pest_name ILIKE '%' || pest || '%'
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Create storage bucket for crop images
INSERT INTO storage.buckets (id, name, public)
VALUES ('crop-images', 'crop-images', true)
ON CONFLICT (id) DO NOTHING;

-- Create storage bucket for heatmaps
INSERT INTO storage.buckets (id, name, public)
VALUES ('heatmaps', 'heatmaps', true)
ON CONFLICT (id) DO NOTHING;

-- Set up storage policies to allow authenticated users to upload images
CREATE POLICY "Users can upload images"
    ON storage.objects
    FOR INSERT
    WITH CHECK (bucket_id IN ('crop-images', 'heatmaps') AND auth.uid() = owner);

-- Set up storage policies to allow public access to images
CREATE POLICY "Public can view images"
    ON storage.objects
    FOR SELECT
    USING (bucket_id IN ('crop-images', 'heatmaps'));