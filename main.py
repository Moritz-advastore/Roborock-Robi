import asyncio
import sys
from roborock.web_api import RoborockApiClient
from roborock.devices.device_manager import create_device_manager, UserParams

# Windows-safe EventLoop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    email = "shelfcleaning@advasolutions.com"
    password = "Pevzos-2nogdo-qyqbat"

    web_api = RoborockApiClient(username=email)
    user_data = await web_api.pass_login(password=password)

    user_params = UserParams(username=email, user_data=user_data)
    device_manager = await create_device_manager(user_params)
    devices = await device_manager.get_devices()
    if not devices:
        print("Keine Geräte gefunden")
        return

    device = devices[0]

    # Status abfragen
    if device.v1_properties and device.v1_properties.status:
        status = await device.v1_properties.status.refresh()
        print("Status ok")

    # Beispielbefehle (Start, Stop, Dock) — mit send_command
    # Start Reinigung
    await device.v1_properties.rpc_channel.send_command("app_start")
    print("Reinigung gestartet")

    # Stop Reinigung
    await asyncio.sleep(5)  # kurz warten
    await device.v1_properties.rpc_channel.send_command("app_stop")
    print("Reinigung gestoppt")

    # Zur Dock zurückfahren
    await device.v1_properties.rpc_channel.send_command("app_charge")
    print("Dock‑Befehl gesendet")

if __name__ == "__main__":
    asyncio.run(main())
