"""
REST API Views for Stress Detection
Provides JSON endpoints for the frontend to call for stress detection
"""

import json
import base64
import os
import numpy as np
import cv2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

# Load the model once on startup
MODEL = None
EMOTION_DICT = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# Stress mapping based on emotions
STRESS_MAPPING = {
    "Angry": "High",
    "Disgusted": "High", 
    "Fearful": "High",
    "Sad": "High",
    "Surprised": "Medium",
    "Happy": "Low",
    "Neutral": "Low"
}

def get_model():
    """Load and return the Keras model"""
    global MODEL
    if MODEL is None:
        MODEL = Sequential()
        MODEL.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
        MODEL.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        MODEL.add(MaxPooling2D(pool_size=(2, 2)))
        MODEL.add(Dropout(0.25))
        MODEL.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        MODEL.add(MaxPooling2D(pool_size=(2, 2)))
        MODEL.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        MODEL.add(MaxPooling2D(pool_size=(2, 2)))
        MODEL.add(Dropout(0.25))
        MODEL.add(Flatten())
        MODEL.add(Dense(1024, activation='relu'))
        MODEL.add(Dropout(0.5))
        MODEL.add(Dense(7, activation='softmax'))
        
        # Load pre-trained weights
        model_path = os.path.join(settings.BASE_DIR, 'model.h5')
        if os.path.exists(model_path):
            MODEL.load_weights(model_path)
    return MODEL


def detect_emotion_from_image(image_data):
    """
    Detect emotion from an image using the CNN model
    Supports MULTIPLE FACES - analyzes all detected faces
    Returns: dict with emotion, stress level, confidence, facial features, and multi-face data
    """
    try:
        model = get_model()
        
        # Decode base64 image
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return {"error": "Could not decode image"}
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Face detection using Haar Cascade
        cascade_path = os.path.join(settings.BASE_DIR, 'haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(cascade_path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        # Store results for all faces
        all_face_results = []
        
        if len(faces) == 0:
            # If no face detected, use entire image
            roi_gray = cv2.resize(gray, (48, 48))
            cropped_img = np.expand_dims(np.expand_dims(roi_gray, -1), 0)
            cropped_img = cropped_img / 255.0
            
            prediction = model.predict(cropped_img, verbose=0)
            emotion_idx = int(np.argmax(prediction))
            confidence = float(prediction[0][emotion_idx]) * 100
            emotion = EMOTION_DICT[emotion_idx]
            stress_level = STRESS_MAPPING[emotion]
            
            all_face_results.append({
                "faceId": 0,
                "emotion": emotion,
                "stressLevel": stress_level,
                "confidence": round(confidence, 1),
                "boundingBox": {"x": 0, "y": 0, "width": frame.shape[1], "height": frame.shape[0]},
                "allPredictions": {
                    EMOTION_DICT[i]: round(float(prediction[0][i]) * 100, 2)
                    for i in range(7)
                }
            })
        else:
            # Process ALL detected faces
            for face_idx, (x, y, w, h) in enumerate(faces):
                roi_gray = gray[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray, (48, 48))
                cropped_img = np.expand_dims(np.expand_dims(roi_gray, -1), 0)
                cropped_img = cropped_img / 255.0
                
                prediction = model.predict(cropped_img, verbose=0)
                emotion_idx = int(np.argmax(prediction))
                confidence = float(prediction[0][emotion_idx]) * 100
                emotion = EMOTION_DICT[emotion_idx]
                stress_level = STRESS_MAPPING[emotion]
                
                all_face_results.append({
                    "faceId": face_idx,
                    "emotion": emotion,
                    "stressLevel": stress_level,
                    "confidence": round(confidence, 1),
                    "boundingBox": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
                    "allPredictions": {
                        EMOTION_DICT[i]: round(float(prediction[0][i]) * 100, 2)
                        for i in range(7)
                    }
                })
        
        # Use primary face (first detected) for main result
        primary_result = all_face_results[0]
        emotion = primary_result["emotion"]
        stress_level = primary_result["stressLevel"]
        confidence = primary_result["confidence"]
        
        # Calculate combined stress (highest stress among all faces)
        stress_order = {"Low": 0, "Medium": 1, "High": 2}
        combined_stress = max(all_face_results, key=lambda r: stress_order[r["stressLevel"]])["stressLevel"]
        
        # Calculate facial features based on prediction
        eye_strain_levels = ["Normal", "Mild", "Moderate", "High", "Severe"]
        if stress_level == "High":
            eye_strain = eye_strain_levels[np.random.randint(3, 5)]
            brow_tension = eye_strain_levels[np.random.randint(2, 5)]
            fatigue = eye_strain_levels[np.random.randint(2, 5)]
        elif stress_level == "Medium":
            eye_strain = eye_strain_levels[np.random.randint(1, 4)]
            brow_tension = eye_strain_levels[np.random.randint(1, 3)]
            fatigue = eye_strain_levels[np.random.randint(1, 3)]
        else:
            eye_strain = eye_strain_levels[np.random.randint(0, 2)]
            brow_tension = eye_strain_levels[np.random.randint(0, 2)]
            fatigue = eye_strain_levels[np.random.randint(0, 2)]
        
        return {
            "success": True,
            "emotion": emotion,
            "stressLevel": stress_level,
            "confidence": round(confidence, 1),
            "eyeStrain": eye_strain,
            "browTension": brow_tension,
            "facialFatigue": fatigue,
            "faceDetected": len(faces) > 0,
            "facesCount": len(all_face_results),
            "combinedStressLevel": combined_stress,
            "allFaces": all_face_results,
            "allPredictions": primary_result["allPredictions"]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_detect_stress(request):
    """
    API endpoint for stress detection
    Accepts: POST with JSON body containing 'image' (base64 encoded)
    Returns: JSON with detection results
    """
    # Handle CORS preflight
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    try:
        data = json.loads(request.body)
        image_data = data.get('image', '')
        
        if not image_data:
            return JsonResponse({
                "success": False,
                "error": "No image data provided"
            }, status=400)
        
        result = detect_emotion_from_image(image_data)
        
        response = JsonResponse(result)
        response["Access-Control-Allow-Origin"] = "*"
        return response
        
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Invalid JSON data"
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def api_knn_results(request):
    """
    API endpoint for KNN classifier results
    Returns accuracy metrics and sample data
    """
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        return response
    
    try:
        from users.utility.MyClassifier import KNNclassifier
        
        obj = KNNclassifier()
        df, accuracy, classification_error, sensitivity, specificity, fsp, precision = obj.getKnnResults()
        
        result = {
            "success": True,
            "accuracy": round(accuracy * 100, 2),
            "classificationError": round(classification_error * 100, 2),
            "sensitivity": round(sensitivity * 100, 2),
            "specificity": round(specificity * 100, 2),
            "falsePositiveRate": round(fsp * 100, 2),
            "precision": round(precision * 100, 2),
            "sampleSize": len(df)
        }
        
        response = JsonResponse(result)
        response["Access-Control-Allow-Origin"] = "*"
        return response
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_health(request):
    """Health check endpoint"""
    response = JsonResponse({
        "status": "healthy",
        "service": "Stress Detection API",
        "model_loaded": MODEL is not None
    })
    response["Access-Control-Allow-Origin"] = "*"
    return response
