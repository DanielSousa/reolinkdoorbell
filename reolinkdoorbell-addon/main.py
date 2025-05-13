import os
import asyncio
import json
import requests
import websockets

# Load config from Home Assistant add-on options
CONFIG_PATH = "/data/options.json"
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Use Docker internal hostname for Home Assistant Core API
HASS_URL = os.environ.get("HASS_URL", "http://homeassistant:8123")
HASS_TOKEN = os.environ.get("HASS_TOKEN", "YOUR_LONG_LIVED_ACCESS_TOKEN")

CAMERA_ENTITY = config["camera_entity"]
LOCK_ENTITY = config["lock_entity"]
TABLET_IP = config["tablet_ip"]
FULLY_KIOSK_PASSWORD = config["fully_kiosk_password"]
DEVICE_CONTROL_METHOD = config["device_control_method"]
MODAL_TIMEOUT = config["modal_timeout"]
DASHBOARD_TAB_PATH = config.get("dashboard_tab_path", "home")

# User must set this to their mobile app notify service (e.g., notify.mobile_app_tablet)
COMPANION_NOTIFY_SERVICE = os.environ.get("COMPANION_NOTIFY_SERVICE", "notify.mobile_app_tablet")

HEADERS = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "Content-Type": "application/json",
}

async def listen_for_doorbell():
    ws_url = HASS_URL.replace("http", "ws") + "/api/websocket"
    async with websockets.connect(ws_url) as ws:
        # Authenticate
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": HASS_TOKEN}))
        await ws.recv()
        print("Connected to Home Assistant WebSocket API.")

        # Subscribe to events
        await ws.send(json.dumps({"id": 1, "type": "subscribe_events", "event_type": "button_press"}))
        print("Subscribed to button_press events.")

        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("type") == "event":
                event = data["event"]
                # Check if event is from the Reolink doorbell
                if event.get("data", {}).get("entity_id") == CAMERA_ENTITY:
                    print("Doorbell pressed!")
                    handle_doorbell_event()


def handle_doorbell_event():
    # 1. Wake tablet
    if DEVICE_CONTROL_METHOD == "fully_kiosk":
        wake_tablet_fully_kiosk()
    elif DEVICE_CONTROL_METHOD == "companion_app":
        wake_tablet_companion_app()
    # 2. Send persistent notification with link to Doorbell tab
    trigger_doorbell_tab_notification()
    # 3. (Optional) Listen for frontend actions (open door, toggle mic)


def wake_tablet_fully_kiosk():
    url = f"http://{TABLET_IP}:2323/?cmd=screenOn&password={FULLY_KIOSK_PASSWORD}"
    try:
        resp = requests.get(url, timeout=3)
        print(f"Woke tablet via Fully Kiosk: {resp.status_code}")
    except Exception as e:
        print(f"Error waking tablet: {e}")

def wake_tablet_companion_app():
    # Send a notification to the Companion App to wake the device
    service_url = f"{HASS_URL}/api/services/{COMPANION_NOTIFY_SERVICE.split('.')[0]}/{COMPANION_NOTIFY_SERVICE.split('.')[1]}"
    payload = {
        "message": "Doorbell pressed!",
        "data": {"command": "wakeup"}
    }
    try:
        resp = requests.post(service_url, headers=HEADERS, json=payload, timeout=3)
        print(f"Sent wakeup notification to Companion App: {resp.status_code}")
    except Exception as e:
        print(f"Error sending Companion App notification: {e}")

def trigger_doorbell_tab_notification():
    # Send a persistent notification with a link to the user-configured dashboard tab
    url_path = f"/lovelace/{DASHBOARD_TAB_PATH}"
    service_url = f"{HASS_URL}/api/services/persistent_notification/create"
    payload = {
        "title": "Doorbell",
        "message": f"Someone is at the door! [View Doorbell Tab]({url_path})",
    }
    try:
        resp = requests.post(service_url, headers=HEADERS, json=payload, timeout=3)
        print(f"Sent persistent notification: {resp.status_code}")
    except Exception as e:
        print(f"Error sending notification: {e}")


if __name__ == "__main__":
    asyncio.run(listen_for_doorbell()) 