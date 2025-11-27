# main_cloud_test.py
# Minimaler Cloud-Test für Roborock S7 Max Ultra
# Prüft Login, listet Geräte, Status und alle v1_properties aus
# Alles, was unklar ist, wird markiert, damit es getestet werden kann

import asyncio
from roborock.web_api import RoborockApiClient
from roborock.devices.device_manager import create_device_manager, UserParams

EMAIL = "shelfcleaning@advasolutions.com"
PASSWORD = "Pevzos-2nogdo-qyqbat"

async def main():
    print("Login via Cloud...")
    web_api = RoborockApiClient(username=EMAIL)
    user_data = await web_api.pass_login(password=PASSWORD)

    # Geräte-Manager erstellen
    user_params = UserParams(username=EMAIL, user_data=user_data)
    device_manager = await create_device_manager(user_params)

    devices = await device_manager.get_devices()
    if not devices:
        print("Keine Geräte gefunden")
        return

    print(f"{len(devices)} Gerät(e) gefunden:\n")

    for i, device in enumerate(devices, start=1):
        print(f"=== Gerät {i} ===")
        print(f"Name: {device.name}")
        print(f"ID (did): {device.duid}")
        print(f"Model: {device._product}")
        print(f"device._device_info {device._device_info}") 
        print(f"device.b01_properties {device.b01_properties}")
        print(f"device._name {device._name}")
        print(f"device.v1_properties {device.v1_properties}")
        print(f"device._channel{device._channel}")
        print(f"device._connect_task{device._connect_task}")


        print("\n--- V1 Properties (explorativ) ---")
        for prop_name in dir(device.v1_properties):
            if not prop_name.startswith("_"):
                try:
                    value = getattr(device.v1_properties, prop_name)
                    print(f"{prop_name}: {value}")
                except Exception as e:
                    print(f"{prop_name}: <konnte nicht ausgelesen werden> ({e})")

        print("\n--- Status auslesen ---")
        try:
            status = await device.v1_properties.status.refresh()
            print("StatusTrait:", status)
        except Exception as e:
            print("Status konnte nicht ausgelesen werden:", e)

        print("\n--- Hinweis zu Start/Stopp/Dock ---")
        print("Um Start/Stopp oder Dock-Befehle zu senden, müssen wir die RPC-Commands")
        print("für dieses Gerät testen. Diese sind nicht direkt dokumentiert.")
        print("Beispiel: device.v1_properties.rpc_channel.send_command('app_start') oder ähnlich\n")

if __name__ == "__main__":
    asyncio.run(main())
