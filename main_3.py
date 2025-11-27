import asyncio
import sys
from pathlib import Path
import pickle

from roborock.web_api import RoborockApiClient
from roborock.devices.device_manager import create_device_manager, UserParams

# Windows-sicheren EventLoop wählen
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKEN_FILE = Path("roborock_userdata.pkl")

async def load_or_login(email: str, password: str):
    """Lädt gespeicherte UserData oder meldet sich neu an."""
    if TOKEN_FILE.exists():
        try:
            with TOKEN_FILE.open("rb") as f:
                user_data = pickle.load(f)
            return user_data
        except Exception:
            pass

    web_api = RoborockApiClient(username=email)
    user_data = await web_api.pass_login(password=password)
    with TOKEN_FILE.open("wb") as f:
        pickle.dump(user_data, f)
    return user_data

async def main():
    email = "shelfcleaning@advasolutions.com"
    password = "Pevzos-2nogdo-qyqbat"

    user_data = await load_or_login(email, password)

    user_params = UserParams(username=email, user_data=user_data)
    device_manager = await create_device_manager(user_params)
    devices = await device_manager.get_devices()

    if not devices:
        print("Keine Geräte gefunden")
        return

    device = devices[0]  # Dein erster Roboter

    # Status abrufen
    await device.v1_properties.status.refresh()
    print("Status:", device.v1_properties.status)

    # Beispiel-Befehle via aktuelle API
    print("Starte Reinigung...")
    await device.send_command("app_start")

    await asyncio.sleep(5)

    print("Stoppe Reinigung...")
    await device.send_command("app_stop")

    print("Zur Dockingstation...")
    await device.send_command("app_charge")

if __name__ == "__main__":
    asyncio.run(main())
