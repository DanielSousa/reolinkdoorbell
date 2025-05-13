# Reolink Doorbell Home Assistant Add-on

[![Open your Home Assistant instance and show the add-ons store.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/DanielSousa/reolinkdoorbell)

Easily integrate your Reolink doorbell with Home Assistant! This add-on listens for doorbell button press events and notifies you with a persistent notification containing a link to your chosen dashboard tab in Home Assistant. It can also wake a tablet running the Home Assistant dashboard using Fully Kiosk Browser or the Companion App.

---

## 🚀 One-Click Install
1. **Click the badge above** or add this repository to your Home Assistant Add-on Store:
   `https://github.com/DanielSousa/reolinkdoorbell`
2. The add-on will appear in the store for one-click install and configuration.

---

## Features
- Detects Reolink doorbell button press via Home Assistant WebSocket API
- Wakes up a wall tablet (Fully Kiosk or Companion App)
- Sends a persistent notification with a link to your chosen dashboard tab
- Configurable camera and lock entities
- Extensible for additional actions and devices

## Configuration
All configuration is done via the Home Assistant add-on UI. No files need to be edited manually.

- `camera_entity`: Camera entity for live video (e.g., `camera.reolink_doorbell`)
- `lock_entity`: Lock or switch entity to open the door (e.g., `lock.front_door`)
- `tablet_ip`: IP address of the wall tablet
- `fully_kiosk_password`: Password for Fully Kiosk REST API
- `device_control_method`: `fully_kiosk` or `companion_app`
- `dashboard_tab_path`: **Path of the dashboard tab where you place the doorbell card** (e.g., `home`, `overview`, `doorbell`). The add-on will use this to build the notification link. Default is `home`.

### Required: Home Assistant Token
You must provide a Home Assistant long-lived access token as an environment variable named `HASS_TOKEN` when running the add-on. See [Home Assistant docs](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token) for how to create one.

### Optional: Companion App Notify Service
If using the Companion App for device wake, set the `COMPANION_NOTIFY_SERVICE` environment variable to your notify service (e.g., `notify.mobile_app_tablet`).

## Setup
1. Install the add-on in Home Assistant Supervisor.
2. Open the add-on UI and configure the options above.
3. Add the doorbell card to your preferred dashboard tab (see below).
4. Set the `dashboard_tab_path` option to match the path of that tab (e.g., `home`, `overview`, `security`).
5. When the doorbell is pressed, you'll receive a persistent notification with a link to that tab (e.g., `/lovelace/home`).

## Example Lovelace Doorbell Card (add to any tab)
```yaml
type: vertical-stack
cards:
  - type: picture-glance
    title: Doorbell
    entities:
      - entity: lock.front_door
    camera_image: camera.reolink_doorbell
    camera_view: live
  - type: horizontal-stack
    cards:
      - type: button
        name: Open Door
        icon: mdi:door-open
        tap_action:
          action: call-service
          service: lock.open
          service_data:
            entity_id: lock.front_door
      - type: button
        name: Toggle Mic
        icon: mdi:microphone
        tap_action:
          action: call-service
          service: script.toggle_reolink_mic  # You must create this script if supported
```

## Security Notes
- Use a Home Assistant long-lived access token for the add-on.
- Restrict add-on permissions to only required APIs/services.
- Secure the Fully Kiosk REST API with a strong password.

## Extensibility
- Add support for multiple tablets/devices
- Add more actions (e.g., toggle mic, custom notifications)
- Customize dashboard card appearance and behavior

## References
- [Reolink Integration](https://www.home-assistant.io/integrations/reolink/)
- [Fully Kiosk Integration](https://www.home-assistant.io/integrations/fully_kiosk/)
- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons/) 