from ultralytics import YOLO
import sys
import os
import numpy as np
import cv2

def detect_objects_from_array(image_array):
    """
    Detect objects in a numpy array image
    
    Args:
        image_array: numpy.ndarray - The image as a numpy array (BGR or RGB format)
    
    Returns:
        list: List of dictionaries containing detected objects with 'class' and 'confidence' keys
    """
    # Load the YOLO model
    model = YOLO('yolov8n.pt')  # Using the smallest YOLOv8 model
    
    # Check if input is a numpy array
    if not isinstance(image_array, np.ndarray):
        print("Error: Input must be a numpy array.")
        return []
    
    # Run inference on the numpy array
    results = model(image_array, verbose=False)
    
    # Process results
    detected_objects = []
    for result in results:
        boxes = result.boxes
        if len(boxes) == 0:
            print("No objects detected in the image.")
            return []
        
        for box in boxes:
            # Get class name and confidence
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            confidence = float(box.conf[0])
            
            # Add object to list
            detected_objects.append({
                'class': class_name,
                'confidence': confidence
            })
    
    return detected_objects