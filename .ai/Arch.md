# Architecture Plan: Reolink Doorbell Addon for Home Assistant

## Goal
Create a Home Assistant add-on that displays a modal with live Reolink video and actionable buttons when the doorbell is pressed, even if the device is in screensaver mode.

---

## 1. Event Detection
- **Trigger:** Detect when the Reolink doorbell button is pressed.
- **Integration:** Use the [Reolink integration](https://www.home-assistant.io/integrations/reolink/) to listen for the `button_press` event or similar trigger.
- **Automation:** Create an automation or a websocket listener in the add-on to respond to this event.

## 2. Screensaver & App Focus Control
- **Device:** Target device is a tablet running the Home Assistant app (assumed Android/iOS/FireOS).
- **Wake Device:** Use [Fully Kiosk Browser](https://www.home-assistant.io/integrations/fully_kiosk/) or [Android TV integration](https://www.home-assistant.io/integrations/androidtv/) to exit screensaver and bring Home Assistant app to foreground.
- **Fallback:** If not using Fully Kiosk, use [Home Assistant Companion App](https://companion.home-assistant.io/) notification commands to wake device and open app.

## 3. Modal UI Overlay
- **Frontend:** Use [Home Assistant Custom Panel](https://developers.home-assistant.io/docs/frontend/custom-ui/) or [Lovelace custom card](https://developers.home-assistant.io/docs/frontend/custom-ui/#custom-cards) to display a modal overlay.
- **Trigger Modal:** Modal is triggered by the event from backend (via websocket or persistent notification).
- **Content:**
  - Live video stream from Reolink camera (use `camera.reolink_*` entity).
  - Buttons: Open Door, Toggle Mic.

## 4. Video Streaming
- **Stream Source:** Use the `camera` entity provided by the Reolink integration.
- **Frontend:** Embed the camera stream in the modal using the `camera_view: live` option or a custom video player if needed.

## 5. Action Buttons
- **Open Door:**
  - Trigger a Home Assistant service (e.g., `lock.open` or `switch.turn_on`) to actuate the door lock.
  - Entity should be configurable.
- **Toggle Mic:**
  - If supported by Reolink integration, send command to enable/disable two-way audio.
  - Otherwise, provide a UI toggle and document limitations.

## 6. Addon Structure
- **Backend:**
  - Listen for doorbell press events.
  - Send frontend trigger (via websocket or persistent notification).
  - Optionally, manage device wake-up via Fully Kiosk/Companion App.
- **Frontend:**
  - Custom panel/card for modal overlay.
  - Handles video stream and button actions.

## 7. Configuration
- **User Options:**
  - Camera entity
  - Door lock entity
  - Device control method (Fully Kiosk, Companion App, etc.)
  - Modal appearance (optional)

## 8. Security & UX
- **Authentication:** Ensure only authorized users/devices can trigger actions.
- **Timeout:** Modal auto-dismiss after configurable time.
- **Accessibility:** Large buttons, clear video, responsive design.

---

## Implementation Plan: Home Assistant Add-on

### 1. Add-on Overview
- The add-on will run as a container managed by Home Assistant Supervisor.
- It will connect to the Home Assistant WebSocket API to listen for Reolink doorbell events.
- On event, it will:
  - Wake the tablet (via Fully Kiosk REST API or Home Assistant service call).
  - Trigger a modal overlay in the Home Assistant UI (by toggling an `input_boolean`, sending a persistent notification, or calling a service).
  - Optionally, listen for "Open Door" and "Toggle Mic" actions and call the appropriate Home Assistant services.

### 2. File Structure
```
reolinkdoorbell-addon/
  Dockerfile
  config.json
  run.sh or main.py
  README.md
```

### 3. Add-on Components
- **Dockerfile:** Defines the environment (Python base image, dependencies).
- **config.json:** Defines user-configurable options (camera entity, lock entity, tablet IP, Fully Kiosk password, etc.).
- **main.py:** Main logic:
  - Connect to Home Assistant WebSocket API.
  - Listen for doorbell press events.
  - On event:
    - Call Fully Kiosk API to wake device.
    - Call Home Assistant service to show modal (toggle `input_boolean`, send persistent notification, etc.).
    - Optionally, listen for frontend actions (e.g., via webhook or Home Assistant events) to open door or toggle mic.
- **README.md:** Usage and configuration instructions.

### 4. Integration Points
- **Home Assistant WebSocket API:** For event listening and service calls.
- **Fully Kiosk REST API:** For waking the tablet and controlling screensaver.
- **Home Assistant Services:** To trigger modal overlay and perform actions (open door, toggle mic).

### 5. Modal Overlay Implementation
- The add-on triggers a modal by toggling an `input_boolean` or sending a persistent notification.
- The Lovelace dashboard uses a conditional card to display the modal when the boolean is on.
- The modal includes:
  - Live camera stream (`camera.reolink_*` entity).
  - Action buttons (call Home Assistant services for door/mic).

### 6. Example Workflow
1. Doorbell button is pressed (event detected via WebSocket API).
2. Add-on calls Fully Kiosk API to wake the tablet.
3. Add-on calls Home Assistant service to toggle `input_boolean.doorbell_active`.
4. Lovelace dashboard shows modal overlay with video and buttons.
5. User presses "Open Door" or "Toggle Mic"; Home Assistant handles the action.
6. Modal auto-dismisses after timeout (handled by automation or add-on).

### 7. Security Considerations
- Use Home Assistant long-lived access tokens for API authentication.
- Restrict add-on permissions to only required APIs/services.
- Validate all configuration inputs.

### 8. Extensibility
- Add support for multiple tablets/devices.
- Add configuration for custom modal appearance or additional actions.

---

## References
- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons/)
- [Reolink Integration](https://www.home-assistant.io/integrations/reolink/)
- [Fully Kiosk Integration](https://www.home-assistant.io/integrations/fully_kiosk/)
- [Custom Panels](https://developers.home-assistant.io/docs/frontend/custom-ui/)
- [Camera Streaming](https://www.home-assistant.io/integrations/camera/) 