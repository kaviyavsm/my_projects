# simulated_smart_parking_system.py

from flask import Flask, jsonify, render_template
import random
import threading
import time

# Initialize Flask app
app = Flask(__name__)

# ----------------------------
# CONFIGURATION
# ----------------------------

NUM_SLOTS = 4                  # Total number of parking slots
car_count = 0                   # Number of cars currently inside
car_count_lock = threading.Lock()  # Lock for thread-safe car counter

# Create mock data for parking slots
PARKING_SLOTS = [
    {
        "id": i + 1,
        "ultrasonic_distance_cm": random.uniform(5, 30),
        "ultrasonic_occupied": False,
        "camera_occupied": False,
        "final_occupied": False
    } for i in range(NUM_SLOTS)
]

# ----------------------------
# SIMULATION FUNCTIONS
# ----------------------------

def simulate_entry_exit_gate():
    """
    Simulate car entering and exiting the parking lot.
    Runs in a loop to mimic real traffic.
    """
    global car_count
    while True:
        time.sleep(random.randint(5, 10))  # Wait 5–10 seconds

        action = random.choice(["entry", "exit"])
        with car_count_lock:
            if action == "entry":
                if car_count < NUM_SLOTS:
                    car_count += 1
                    print("Simulated: Car ENTERED")
            elif action == "exit":
                if car_count > 0:
                    car_count -= 1
                    print("Simulated: Car EXITED")

def simulate_parking_slots():
    """
    Simulate slot status using mock sensor readings.
    """
    while True:
        time.sleep(3)
        for slot in PARKING_SLOTS:
            # Simulate ultrasonic distance (5 = close = occupied, 30 = far = empty)
            slot["ultrasonic_distance_cm"] = round(random.uniform(5, 30), 2)
            slot["ultrasonic_occupied"] = slot["ultrasonic_distance_cm"] < 10

            # Simulate camera logic (random true/false)
            slot["camera_occupied"] = random.choice([True, False])

            # Final decision: if either says occupied, it's taken
            slot["final_occupied"] = slot["ultrasonic_occupied"] or slot["camera_occupied"]

# ----------------------------
# FLASK ROUTES
# ----------------------------

@app.route("/")
def dashboard():
    """
    Serve the real-time dashboard page.
    """
    return render_template("dashboard.html", slots=PARKING_SLOTS, car_count=car_count, total_slots=NUM_SLOTS)

@app.route("/parking-status", methods=["GET"])
def parking_status():
    """
    Returns JSON with:
    - current car count
    - total & available slots
    - status for each slot
    """
    with car_count_lock:
        available_slots = max(0, NUM_SLOTS - car_count)

    return jsonify({
        "car_count": car_count,
        "available_slots": available_slots,
        "total_slots": NUM_SLOTS,
        "slots": [
            {
                "slot_id": slot["id"],
                "ultrasonic_distance_cm": slot["ultrasonic_distance_cm"],
                "ultrasonic_occupied": slot["ultrasonic_occupied"],
                "camera_occupied": slot["camera_occupied"],
                "final_occupied": slot["final_occupied"]
            } for slot in PARKING_SLOTS
        ]
    })

# ----------------------------
# RUN THE SIMULATION
# ----------------------------

if __name__ == "__main__":
    print("🟢 Starting Smart Parking Simulation...")

    # Start simulated sensor threads
    threading.Thread(target=simulate_entry_exit_gate, daemon=True).start()
    threading.Thread(target=simulate_parking_slots, daemon=True).start()

    # Start Flask API
    app.run(host="0.0.0.0", port=5000)