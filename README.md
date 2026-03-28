# Singapore Bus Arrival Tracker

A Flask-based web application that displays real-time bus arrival times for Singapore bus stops. Features a modern dark-themed UI with auto-refresh and mobile-responsive design.

## Features

- Real-time bus arrival data from LTA DataMall API
- Multiple bus stop support with easy selection
- Auto-refresh countdown (2 minutes)
- Live arrival time updates (recomputes client-side)
- Mobile-responsive design with touch-friendly interface
- JSON API endpoint for programmatic access
- Docker deployment support

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your LTA API key
```

3. Run the application:
```bash
python bus_arrival.py
```

4. Open http://localhost:5000

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Access the application at http://localhost:5000

### Manual Docker Build

```bash
docker build -t bus-arrival-tracker .
docker run -p 5000:5000 --env-file .env bus-arrival-tracker
```

## Configuration

### Bus Stops

Edit `config.json` to add or modify bus stops:

```json
{
  "bus_stops": {
    "84069": {
      "name": "Default Stop",
      "services": ["45", "46"],
      "description": "Example bus stop"
    }
  },
  "default_stop": "84069"
}
```

### Environment Variables

- `LTA_API_KEY`: Your LTA DataMall API key
- `LTA_URL`: LTA API endpoint (optional, defaults to official URL)

## API Endpoints

### Main Dashboard
- `GET /` - Default bus stop dashboard
- `GET /<bus_stop_code>` - Dashboard for specific bus stop
- `GET /?stop=<bus_stop_code>` - Dashboard with query parameter

### JSON API
- `GET /api/bus-arrival` - Get arrival data as JSON
- `GET /api/bus-arrival?stop=<bus_stop_code>` - Get data for specific stop

### Health Check
- `GET /health` - Health check endpoint

## Deployment Options

### Production with Gunicorn

```bash
gunicorn -c gunicorn_config.py bus_arrival:app
```

### Cloud Platforms

#### Heroku
```bash
heroku create
heroku config:set LTA_API_KEY=your_key_here
git push heroku main
```

#### AWS ECS/Fargate
Deploy using the provided Dockerfile and docker-compose.yml

#### Render/Railway/Vercel
Deploy using the Docker image with environment variables set

## Mobile Features

- Single-column layout on devices < 480px
- Touch-friendly tap targets (min 44x44px)
- Responsive header and navigation
- Optimized for portrait mode

## Adding More Bus Stops

1. Get the bus stop code from LTA DataMall
2. Add it to `config.json` under `bus_stops`
3. Specify available services for that stop
4. The UI will automatically update with the new stop

## Troubleshooting

### API Key Issues
- Ensure your LTA API key is valid
- Check API rate limits (500 requests per minute for free tier)

### Docker Issues
- Ensure `.env` file is present
- Check port 5000 is not already in use
- Verify config.json is in the same directory

### Data Not Loading
- Check network connectivity to LTA API
- Verify bus stop code is valid
- Check browser console for JavaScript errors

## License

MIT

## Data Source

Bus arrival data provided by Land Transport Authority (LTA) Singapore via LTA DataMall API.
