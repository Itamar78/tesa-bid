# TESA Bid Server

A FastAPI-based machine learning service that scores text snippets for relevance and provides bidding recommendations.

## Overview

This service uses a pre-trained machine learning model to analyze text snippets and provide:
- **Relevance Score**: Probability of the snippet being relevant (0-1)
- **Bid Decision**: Binary decision (0 or 1) based on relevance threshold
- **Price Recommendation**: Calculated price based on relevance score

## Features

- FastAPI REST API with automatic documentation
- Sentence transformer embeddings for text analysis
- Pre-trained relevance calibration model
- Docker containerization support
- Caching for improved performance

## Project Structure

```
tesa-bid/
├── src/
│   └── serve.py          # FastAPI server implementation
├── models/
│   └── relevance_calibrator.joblib  # Pre-trained ML model
├── Dockerfile            # Container configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## API Endpoints

### POST `/score`

Analyzes a text snippet and returns relevance scoring information.

**Request Body:**
```json
{
  "url": "https://example.com/article",  // Optional
  "snippet": "Your text snippet to analyze"
}
```

**Response:**
```json
{
  "bid": 1,                    // Binary decision (0 or 1)
  "price": 3.245,              // Recommended price
  "score": 0.8234              // Relevance probability (0-1)
}
```

## Quick Start

### Option 1: Using Docker (Recommended)

1. **Build the Docker image:**
   ```bash
   docker build -t tesa-bid-server .
   ```

2. **Run the container:**
   ```bash
   docker run -p 9000:9000 tesa-bid-server
   ```

3. **Test the API:**
   ```bash
   curl -X POST "http://localhost:9000/score" \
        -H "Content-Type: application/json" \
        -d '{"snippet": "Machine learning and AI technologies are transforming industries"}'
   ```

### Option 2: Local Python Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python3 src/serve.py
   ```

3. **Access the API:**
   - API: `http://localhost:9000`
   - Interactive docs: `http://localhost:9000/docs`

## Docker Commands

### Basic Operations
```bash
# Build image
docker build -t tesa-bid-server .

# Run container
docker run -p 9000:9000 tesa-bid-server

# Run in background
docker run -d -p 9000:9000 --name tesa-bid tesa-bid-server

# Stop container
docker stop tesa-bid

# Remove container
docker rm tesa-bid

# View logs
docker logs tesa-bid
```

### Development
```bash
# Run with interactive shell
docker run -it -p 9000:9000 tesa-bid-server /bin/bash

# Run with volume mounting for development
docker run -p 9000:9000 -v $(pwd)/src:/app/src tesa-bid-server
```

## API Usage Examples

### Basic Scoring
```bash
curl -X POST "http://localhost:9000/score" \
     -H "Content-Type: application/json" \
     -d '{"snippet": "Latest developments in artificial intelligence"}'
```

### With URL
```bash
curl -X POST "http://localhost:9000/score" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://techcrunch.com/ai-news",
       "snippet": "Breaking: New AI model achieves 95% accuracy"
     }'
```

### Using Python requests
```python
import requests

response = requests.post(
    "http://localhost:9000/score",
    json={"snippet": "Machine learning breakthrough"}
)
result = response.json()
print(f"Bid: {result['bid']}, Price: {result['price']}, Score: {result['score']}")
```

## Model Details

- **Embedding Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Classification Model**: Pre-trained relevance calibrator (joblib format)
- **Threshold**: 0.354374 for binary classification
- **Price Range**: 0.5 to 6.0 (scaled by relevance score)

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Sentence Transformers**: Text embeddings
- **Scikit-learn**: Machine learning utilities
- **Joblib**: Model serialization
- **NumPy**: Numerical computing
- **Pydantic**: Data validation

## Configuration

The server runs on:
- **Host**: 0.0.0.0 (accepts connections from any IP)
- **Port**: 9000
- **Model Path**: Automatically resolved relative to project structure

## Performance

- **Caching**: Text embeddings are cached (LRU cache, max 20,000 entries)
- **Model Loading**: Models loaded once at startup
- **Response Time**: Typically < 100ms for text analysis

## Troubleshooting

### Common Issues

1. **Model not found**: Ensure `models/relevance_calibrator.joblib` exists
2. **Port already in use**: Change port mapping: `-p 9001:9000`
3. **Dependencies missing**: Run `pip install -r requirements.txt`

### Debugging

```bash
# Check container logs
docker logs tesa-bid

# Access container shell
docker exec -it tesa-bid /bin/bash

# Test connectivity
curl http://localhost:9000/docs
```
