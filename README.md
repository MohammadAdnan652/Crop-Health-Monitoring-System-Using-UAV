# UAV Image Analysis Platform

A comprehensive web-based platform for analyzing aerial images captured by UAVs (drones). This platform provides advanced computer vision capabilities for agricultural and environmental monitoring.

## Features

### 🖼️ Image Stitching
- Combine multiple overlapping drone images into a single panoramic view
- Automatic image alignment and blending
- Support for various image formats (JPG, PNG)

### 🌳 Tree Counting
- Automated detection and counting of trees in aerial images
- Contour-based analysis with configurable thresholds
- Visual output with detected trees highlighted

### 🗺️ Area Detection
- Identify and map crop areas and vegetation zones
- Bounding box detection for spatial analysis
- Support for large-scale agricultural monitoring

### 🐛 Disease Detection
- Early detection of plant diseases using color analysis
- HSV color space processing for accurate detection
- Configurable detection parameters

### 📊 Object Counting
- Count green objects and vegetation in filtered images
- Area-based filtering to remove noise
- Statistical analysis and reporting

## Technology Stack

- **Backend**: Python Flask
- **Computer Vision**: OpenCV, NumPy
- **Image Processing**: PIL, imutils
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Deployment**: Docker, Docker Compose
- **Server**: Gunicorn

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for containerized deployment)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Project\ UAV
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - The web interface will be available for image upload and processing

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - The application will be running in a containerized environment

### Manual Docker Build

1. **Build the Docker image**
   ```bash
   docker build -t uav-analysis .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/processed:/app/processed uav-analysis
   ```

## API Endpoints

### Base URL: `http://localhost:5000`

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/` | GET | Web interface | None |
| `/api` | GET | API information | None |
| `/stitch` | POST | Stitch multiple images | `images` (multiple files) |
| `/count-trees` | POST | Count trees in image | `image` (single file) |
| `/detect-areas` | POST | Detect crop areas | `image` (single file) |
| `/detect-diseases` | POST | Detect plant diseases | `image` (single file) |
| `/count-objects` | POST | Count green objects | `image` (single file) |

### Example API Usage

```bash
# Stitch multiple images
curl -X POST -F "images=@image1.jpg" -F "images=@image2.jpg" http://localhost:5000/stitch

# Count trees in an image
curl -X POST -F "image=@aerial_image.jpg" http://localhost:5000/count-trees

# Detect areas in an image
curl -X POST -F "image=@field_image.jpg" http://localhost:5000/detect-areas
```

## Project Structure

```
Project UAV/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Uploaded images (created automatically)
├── processed/            # Processed results (created automatically)
├── area_detection/       # Area detection algorithms
├── count_trees/          # Tree counting algorithms
├── Count_new/            # Object counting algorithms
├── Image Stitching/      # Image stitching algorithms
├── images_nadir_RGB/     # Sample drone images
└── data_csv/             # CSV data files
```

## Configuration

### Environment Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)

### Algorithm Parameters

You can modify the detection parameters in the respective functions:

- **Tree Counting**: Adjust `min_area` threshold in `count_trees()` function
- **Disease Detection**: Modify HSV color ranges in `detect_diseases()` function
- **Object Counting**: Change `min_area_threshold` in `count_objects()` function

## Deployment Options

### 1. Local Development
- Best for development and testing
- Direct access to source code
- Easy debugging

### 2. Docker Deployment
- Consistent environment across platforms
- Easy scaling and management
- Production-ready configuration

### 3. Cloud Deployment

#### Heroku
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy to Heroku
heroku create your-uav-app
git push heroku main
```

#### AWS EC2
```bash
# Install Docker on EC2
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Deploy application
docker-compose up -d
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/uav-analysis
gcloud run deploy --image gcr.io/PROJECT_ID/uav-analysis --platform managed
```

## Performance Optimization

### For Large Images
- Resize images before processing
- Use batch processing for multiple images
- Implement caching for repeated operations

### For High Traffic
- Use load balancers
- Implement Redis caching
- Scale horizontally with multiple containers

## Troubleshooting

### Common Issues

1. **OpenCV Installation Issues**
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install libgl1-mesa-glx libglib2.0-0
   
   # On Windows
   pip install opencv-python-headless
   ```

2. **Memory Issues with Large Images**
   - Reduce image resolution before processing
   - Increase Docker memory limits
   - Use image compression

3. **Docker Build Failures**
   ```bash
   # Clean Docker cache
   docker system prune -a
   docker build --no-cache -t uav-analysis .
   ```

### Logs and Debugging

```bash
# View application logs
docker-compose logs uav-app

# Access container shell
docker exec -it <container_id> /bin/bash

# Monitor resource usage
docker stats
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section

## Future Enhancements

- [ ] Machine learning-based object detection
- [ ] Real-time video processing
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Integration with GIS systems
- [ ] Multi-spectral image support 