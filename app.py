import os
import cv2
import numpy as np
import imutils
import glob
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import base64
from PIL import Image
import io
import json

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG', 'JPEG', 'PNG'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def save_base64_image(base64_string, filename):
    """Save base64 image to file"""
    image_data = base64.b64decode(base64_string)
    with open(filename, 'wb') as f:
        f.write(image_data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api')
def api_info():
    return jsonify({
        "message": "UAV Image Analysis API",
        "status": "running",
        "endpoints": {
            "stitch_images": "/stitch",
            "count_trees": "/count-trees",
            "detect_areas": "/detect-areas",
            "detect_diseases": "/detect-diseases",
            "count_objects": "/count-objects"
        }
    })

@app.route('/test', methods=['POST'])
def test_endpoint():
    """Test endpoint to verify backend is working"""
    print("=== TEST ENDPOINT CALLED ===")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request files: {request.files}")
    print(f"Request form: {request.form}")
    
    return jsonify({
        "success": True,
        "message": "Backend is working correctly",
        "received_files": len(request.files),
        "received_form_data": len(request.form)
    })

@app.route('/stitch', methods=['POST'])
def stitch_images():
    """Stitch multiple images together"""
    try:
        print("=== STITCH ENDPOINT CALLED ===")
        print(f"Request files: {request.files}")
        print(f"Request form: {request.form}")
        
        if 'images' not in request.files:
            print("ERROR: No 'images' in request.files")
            return jsonify({"error": "No images provided"}), 400
        
        files = request.files.getlist('images')
        print(f"Files received: {len(files)} files")
        
        if not files or files[0].filename == '':
            print("ERROR: No files selected or empty filename")
            return jsonify({"error": "No images selected"}), 400
        
        images = []
        for i, file in enumerate(files):
            print(f"Processing file {i+1}: {file.filename}")
            if file and allowed_file(file.filename):
                # Read image directly from file
                file_bytes = file.read()
                print(f"File {i+1} size: {len(file_bytes)} bytes")
                nparr = np.frombuffer(file_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if img is not None:
                    print(f"File {i+1} loaded successfully, shape: {img.shape}")
                    images.append(img)
                else:
                    print(f"ERROR: Could not decode file {i+1}")
            else:
                print(f"ERROR: File {i+1} not allowed or invalid")
        
        if len(images) < 2:
            return jsonify({"error": "At least 2 images required for stitching"}), 400
        
        # Create image stitcher
        imageStitcher = cv2.Stitcher_create()
        error, stitched_img = imageStitcher.stitch(images)
        
        if error:
            return jsonify({"error": "Images could not be stitched. Not enough keypoints detected."}), 400
        
        # Process the stitched image
        stitched_img = cv2.copyMakeBorder(stitched_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0,0,0))
        gray = cv2.cvtColor(stitched_img, cv2.COLOR_BGR2GRAY)
        thresh_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
        
        contours = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        
        if contours:
            areaOI = max(contours, key=cv2.contourArea)
            mask = np.zeros(thresh_img.shape, dtype="uint8")
            x, y, w, h = cv2.boundingRect(areaOI)
            cv2.rectangle(mask, (x,y), (x + w, y + h), 255, -1)
            
            minRectangle = mask.copy()
            sub = mask.copy()
            
            while cv2.countNonZero(sub) > 0:
                minRectangle = cv2.erode(minRectangle, None)
                sub = cv2.subtract(minRectangle, thresh_img)
            
            contours = cv2.findContours(minRectangle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            
            if contours:
                areaOI = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(areaOI)
                stitched_img = stitched_img[y:y + h, x:x + w]
        
        # Save processed image
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], 'stitched_output.png')
        cv2.imwrite(output_path, stitched_img)
        
        # Convert to base64 for response
        _, buffer = cv2.imencode('.png', stitched_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            "success": True,
            "message": "Images stitched successfully",
            "image": img_base64,
            "output_path": output_path
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/count-trees', methods=['POST'])
def count_trees():
    """Count trees in an image"""
    try:
        print("=== COUNT TREES ENDPOINT CALLED ===")
        print(f"Request files: {request.files}")
        
        if 'image' not in request.files:
            print("ERROR: No 'image' in request.files")
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("ERROR: Empty filename")
            return jsonify({"error": "No image selected"}), 400
        
        if file and allowed_file(file.filename):
            # Read image
            file_bytes = file.read()
            nparr = np.frombuffer(file_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return jsonify({"error": "Invalid image file"}), 400
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply adaptive thresholding
            binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours based on area
            min_area = 1000
            valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
            
            # Draw contours on the original image
            img_contours = cv2.drawContours(img.copy(), valid_contours, -1, (0, 255, 0), 2)
            
            # Count trees
            num_trees = len(valid_contours)
            
            # Save result image
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], 'detected_trees.png')
            cv2.imwrite(output_path, img_contours)
            
            # Convert to base64
            _, buffer = cv2.imencode('.png', img_contours)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                "success": True,
                "tree_count": num_trees,
                "image": img_base64,
                "output_path": output_path
            })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/detect-areas', methods=['POST'])
def detect_areas():
    """Detect crops and trees in an image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        if file and allowed_file(file.filename):
            # Read image
            file_bytes = file.read()
            nparr = np.frombuffer(file_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return jsonify({"error": "Invalid image file"}), 400
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply thresholding
            _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Draw contours
            result = img.copy()
            cv2.drawContours(result, contours, -1, (0, 255, 0), 2)
            
            # Calculate bounding boxes
            boxes = [cv2.boundingRect(cnt) for cnt in contours]
            
            # Save result image
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], 'detected_areas.png')
            cv2.imwrite(output_path, result)
            
            # Convert to base64
            _, buffer = cv2.imencode('.png', result)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                "success": True,
                "detected_areas": len(boxes),
                "bounding_boxes": boxes,
                "image": img_base64,
                "output_path": output_path
            })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/detect-diseases', methods=['POST'])
def detect_diseases():
    """Detect diseases in an image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        if file and allowed_file(file.filename):
            # Read image
            file_bytes = file.read()
            nparr = np.frombuffer(file_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return jsonify({"error": "Invalid image file"}), 400
            
            # Convert to HSV
            hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Define color range for disease detection
            lower_color = np.array([0, 50, 50])
            upper_color = np.array([10, 255, 255])
            
            # Create mask
            mask = cv2.inRange(hsv_image, lower_color, upper_color)
            
            # Apply blurring and morphological operations
            blurred = cv2.GaussianBlur(mask, (11, 11), 0)
            kernel = np.ones((5, 5), np.uint8)
            morphed = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours
            min_area = 100
            max_area = 1000
            detected_diseases = [cnt for cnt in contours if min_area < cv2.contourArea(cnt) < max_area and cv2.isContourConvex(cnt)]
            
            # Draw contours
            result_image = img.copy()
            cv2.drawContours(result_image, detected_diseases, -1, (0, 255, 0), 2)
            
            # Save result image
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], 'detected_diseases.png')
            cv2.imwrite(output_path, result_image)
            
            # Convert to base64
            _, buffer = cv2.imencode('.png', result_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                "success": True,
                "disease_count": len(detected_diseases),
                "image": img_base64,
                "output_path": output_path
            })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/count-objects', methods=['POST'])
def count_objects():
    """Count green objects in an image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        if file and allowed_file(file.filename):
            # Read image
            file_bytes = file.read()
            nparr = np.frombuffer(file_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return jsonify({"error": "Invalid image file"}), 400
            
            # Convert to grayscale
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply binary threshold
            _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter by area
            min_area_threshold = 2000
            large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area_threshold]
            
            # Count objects
            object_count = len(large_contours)
            
            # Draw contours
            result_image = img.copy()
            cv2.drawContours(result_image, large_contours, -1, (0, 255, 0), 2)
            
            # Save result image
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], 'counted_objects.png')
            cv2.imwrite(output_path, result_image)
            
            # Convert to base64
            _, buffer = cv2.imencode('.png', result_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                "success": True,
                "object_count": object_count,
                "image": img_base64,
                "output_path": output_path
            })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 