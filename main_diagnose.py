# main_diagnose.py
import asyncio
from pathlib import Path
from roborock.web_api import RoborockApiClient
from roborock.devices.device_manager import create_device_manager, UserParams

EMAIL = 'shelfcleaning@advasolutions.com'
PASSWORD = 'Pevzos-2nogdo-qyqbat'

TOKEN_FILE = Path('user_token.json')

async def login_once(email: str, password: str):
    """Login über Cloud und speichere UserData in Datei."""
    web_api = RoborockApiClient(username=email)
    user_data = await web_api.pass_login(password=password)
    TOKEN_FILE.write_text(str(user_data))  # UserData nicht JSON, einfach str
    return user_data

async def main():
    if TOKEN_FILE.exists():
        print("Token vorhanden, versuche Login...")
        # In echten Skripten könntest du hier laden und wiederverwenden
        # Für Diagnose: immer neu einloggen
    print("Login...")
    user_data = await login_once(EMAIL, PASSWORD)
    
    user_params = UserParams(username=EMAIL, user_data=user_data)
    device_manager = await create_device_manager(user_params)
    devices = await device_manager.get_devices()
    
    if not devices:
        print("Keine Geräte gefunden")
        return
    
    print(f"{len(devices)} Gerät(e) gefunden:")
    for idx, device in enumerate(devices):
        print(f"\n=== Gerät {idx+1} ===")
        print(f"Name: {device.name}, Modell: {device.product_model}, ID: {device.did}")
        print("Verfügbare Traits in v1_properties:")
        traits = dir(device.v1_properties)
        print(", ".join(traits))
        
        # Status abrufen
        if hasattr(device.v1_properties, 'status'):
            print("\nStatus abrufen...")
            status_trait = device.v1_properties.status
            await status_trait.refresh()
            print(status_trait)
        else:
            print("Kein Status-Trait verfügbar")

if __name__ == "__main__":
    asyncio.run(main())
