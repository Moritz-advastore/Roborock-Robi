import asyncio
import json
import sys
from pathlib import Path
from roborock.web_api import RoborockApiClient
from roborock.devices.device_manager import create_device_manager, UserParams

# Windows-safe EventLoop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKEN_FILE = Path("roborock_token.json")

async def login_once(email, password):
    """Logge einmal ein, speichere Token in Datei"""
    if TOKEN_FILE.exists():
        data = json.loads(TOKEN_FILE.read_text())
        return data
    web_api = RoborockApiClient(username=email)
    user_data = await web_api.pass_login(password=password)
    TOKEN_FILE.write_text(json.dumps(user_data))
    return user_data

async def main():
    email = "shelfcleaning@advasolutions.com"
    password = "Pevzos-2nogdo-qyqbat"

    # Einloggen / Token wiederverwenden
    user_data = await login_once(email, password)

    # Geräte-Manager
    user_params = UserParams(username=email, user_data=user_data)
    device_manager = await create_device_manager(user_params)
    devices = await device_manager.get_devices()
    if not devices:
        print("Keine Geräte gefunden")
        return

    device = devices[0]

    # Status abfragen
    if device.v1_properties and device.v1_properties.status:
        await device.v1_properties.status.refresh()
        print("Status abgerufen:", device.v1_properties.status)

    # Beispielbefehle (RPC)
    await device.v1_properties.rpc_channel.send_command("app_start")
    print("Reinigung gestartet")
    await asyncio.sleep(5)
    await device.v1_properties.rpc_channel.send_command("app_stop")
    print("Reinigung gestoppt")
    await device.v1_properties.rpc_channel.send_command("app_charge")
    print("Dock-Befehl gesendet")

if __name__ == "__main__":
    asyncio.run(main())
