# OpenFilter YOLO Example

A real-time object detection pipeline using OpenFilter, YOLOv8, and PostgreSQL. This project demonstrates how to build a video processing pipeline that detects objects in video streams and logs person count changes to a database.

## 🎯 Features

- **Real-time Object Detection**: Uses YOLOv8 to detect objects in video streams
- **Database Logging**: Automatically logs person count changes to PostgreSQL
- **Web Visualization**: View the processed video stream in a web browser
- **Modular Pipeline**: Built with OpenFilter's modular filter architecture

## 🏗️ Architecture

The pipeline consists of four main components:

1. **VideoIn Filter**: Reads video from file (loops the example video)
2. **YOLO Filter**: Performs object detection using YOLOv8
3. **DB Filter**: Counts objects, logs person count changes to database, and adds text overlay
4. **Webvis Filter**: Provides web-based visualization of the processed stream

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL database
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/PlainsightAI/openfilter-tutorial.git
cd openfilter-tutorial
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
### 4. Database Setup

Create a PostgreSQL database and table:

```sql
CREATE DATABASE openfilter_example;
\c openfilter_example;

CREATE TABLE openfilter_example (
    id SERIAL PRIMARY KEY,
    current_count INTEGER NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Environment Configuration

Create a `.env` file in the project root:

```env
user=postgres
password=your_password
host=localhost
port=5432
dbname=openfilter_example
```

### 6. Run the Pipeline

```bash
python run.py
```

## 🌐 Access the Web Interface

Once running, open your browser and navigate to:
```
http://localhost:8080
```

You should see the processed video stream with object detection overlays and real-time object counts.

## 📁 Project Structure

```
openfilter-tutorial/
├── run.py              # Main pipeline runner
├── filters/            # Custom filter implementations
│   ├── filter_yolo.py  # YOLO object detection filter
│   └── filter_db.py    # Database logging filter
├── utils/              # Utility functions
│   └── detect_object.py # YOLO detection utilities
├── requirements.txt    # Python dependencies
├── yolov8n.pt         # YOLOv8 model file
├── example_video.mp4  # Sample video for testing
├── .env               # Database configuration (create this)
├── logs/              # Application logs
└── README.md          # This file
```

## 🔧 Configuration

### Database Configuration

The database connection is configured via environment variables in `.env`:

- `user`: PostgreSQL username (default: postgres)
- `password`: PostgreSQL password
- `host`: Database host (default: localhost)
- `port`: Database port (default: 5432)
- `dbname`: Database name (default: postgres)

### Filter Configuration

Each filter can be configured by modifying the parameters in `run.py`:

- **VideoIn**: Change video source, enable/disable loop
  - **Video Sources**: The VideoIn filter supports multiple input formats:
    - `file://path/to/video.mp4` - Local video files
    - `file://path/to/video.mp4!loop` - Loop the video continuously
    - `rtsp://path:port/name` - RTSP streams
    - `webcam://0` - First webcam device
    - `webcam://1` - Second webcam device (if available)
- **YOLOFilter**: Adjust detection confidence thresholds
- **DBFilter**: Modify person count logging logic
- **Webvis**: Change web interface port and settings

## 📊 What Gets Logged

The database logs person count changes with the following information:
- `current_count`: Number of people detected
- `notes`: Description of the change (increase/decrease)
- `created_at`: Timestamp of the event

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify PostgreSQL is running
   - Check `.env` file configuration
   - Ensure database and table exist

2. **YOLO Model Not Found**
   - Download `yolov8n.pt` from Ultralytics releases
   - Place it in the project root directory

3. **Port Already in Use**
   - Change port numbers in `run.py` if needed
   - Check if other services are using the same ports

4. **Video Not Playing**
   - Ensure `example_video.mp4` exists in the project root
   - Check video file format compatibility


## 🙏 Acknowledgments

- [OpenFilter](https://github.com/openfilter/openfilter) - Video processing framework
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection model
- [PostgreSQL](https://www.postgresql.org/) - Database system 