from flask import Flask, jsonify, render_template, request
import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- Config ---
API_KEY = os.getenv("LTA_API_KEY")
LTA_URL = os.getenv("LTA_URL", "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival")

with open("config.json", "r") as f:
    config = json.load(f)

headers = {
    "AccountKey": API_KEY,
    "accept": "application/json"
}


def format_arrival(estimated_arrival):
    """Convert the arrival datetime string into minutes from now."""
    if not estimated_arrival:
        return None
    try:
        arrival_time = datetime.fromisoformat(estimated_arrival)
        now = datetime.now(arrival_time.tzinfo)
        diff_seconds = (arrival_time - now).total_seconds()
        diff_minutes = int(diff_seconds // 60)

        if diff_minutes < 1:
            return "Arr"
        return str(diff_minutes)
    except Exception:
        return None


def parse_bus(bus_data):
    """Pull out the useful info from each NextBus block."""
    if not bus_data or not bus_data.get("EstimatedArrival"):
        return None

    load_map = {
        "SEA": {"label": "Seats Available", "level": "low"},
        "SDA": {"label": "Standing Available", "level": "medium"},
        "LSD": {"label": "Limited Standing", "level": "high"},
    }
    load_raw = bus_data.get("Load", "")
    load_info = load_map.get(load_raw, {"label": load_raw, "level": "unknown"})

    type_map = {
        "SD": "Single Deck",
        "DD": "Double Deck",
        "BD": "Bendy",
    }
    bus_type = type_map.get(bus_data.get("Type", ""), bus_data.get("Type", ""))

    return {
        "estimated_arrival": bus_data.get("EstimatedArrival"),
        "minutes_away": format_arrival(bus_data.get("EstimatedArrival")),
        "load_label": load_info["label"],
        "load_level": load_info["level"],
        "type": bus_type,
        "wheelchair": bus_data.get("Feature") == "WAB",
        "monitored": bus_data.get("Monitored") == 1,
    }


def fetch_arrivals(bus_stop_code, bus_services):
    """Fetch and parse bus arrival data from LTA."""
    try:
        response = requests.get(
            LTA_URL,
            headers=headers,
            params={"BusStopCode": bus_stop_code},
            timeout=5
        )

        if response.status_code != 200:
            return None, f"LTA API returned status {response.status_code}"

        data = response.json()
        services = data.get("Services", [])

        result = {}
        for service in services:
            service_no = service.get("ServiceNo")
            if service_no in bus_services:
                result[service_no] = {
                    "operator": service.get("Operator"),
                    "next_bus": parse_bus(service.get("NextBus")),
                    "next_bus_2": parse_bus(service.get("NextBus2")),
                    "next_bus_3": parse_bus(service.get("NextBus3")),
                }

        # Add placeholder for buses with no data
        for bus in bus_services:
            if bus not in result:
                result[bus] = None

        return result, None

    except requests.exceptions.Timeout:
        return None, "Request to LTA API timed out"
    except Exception as e:
        return None, str(e)


# --- Routes ---

@app.route("/")
@app.route("/<bus_stop_code>")
def index(bus_stop_code=None):
    """Render the bus arrival dashboard."""
    # Get bus stop from parameter, query string, or default
    bus_stop_code = bus_stop_code or request.args.get("stop") or config["default_stop"]
    
    # Validate bus stop exists in config
    if bus_stop_code not in config["bus_stops"]:
        bus_stop_code = config["default_stop"]
    
    bus_stop_info = config["bus_stops"][bus_stop_code]
    bus_services = bus_stop_info["services"]
    
    arrivals, error = fetch_arrivals(bus_stop_code, bus_services)
    
    return render_template(
        "index.html",
        bus_stop=bus_stop_code,
        bus_stop_info=bus_stop_info,
        bus_services=bus_services,
        arrivals=arrivals,
        error=error,
        fetched_at=datetime.now().strftime("%d %b %Y, %I:%M:%S %p"),
        all_bus_stops=config["bus_stops"]
    )


@app.route("/api/bus-arrival", methods=["GET"])
def bus_arrival_api():
    """JSON API endpoint for programmatic access."""
    bus_stop_code = request.args.get("stop", config["default_stop"])
    
    if bus_stop_code not in config["bus_stops"]:
        bus_stop_code = config["default_stop"]
    
    bus_services = config["bus_stops"][bus_stop_code]["services"]
    
    arrivals, error = fetch_arrivals(bus_stop_code, bus_services)
    if error:
        return jsonify({"error": error}), 502
    return jsonify({
        "bus_stop": bus_stop_code,
        "bus_stop_info": config["bus_stops"][bus_stop_code],
        "fetched_at": datetime.now().isoformat(),
        "arrivals": arrivals
    })


@app.route("/health", methods=["GET"])
def health():
    """Simple health check."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
