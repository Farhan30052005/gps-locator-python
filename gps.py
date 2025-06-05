# Importing Necessary Modules
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import folium
import datetime
import time
import os
from pathlib import Path

# This method will return your actual coordinates using your IP address
def locationCoordinates():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        return lat, long, city, state
    except requests.RequestException as e:
        print("Error fetching location:", e)
        exit()

# This method fetches coordinates and creates an HTML map file
def gps_locator():
    obj = folium.Map(location=[0, 0], zoom_start=2)

    try:
        lat, long, city, state = locationCoordinates()
        print(f"\n📍 You are in {city}, {state}")
        print(f"🌐 Latitude = {lat}, Longitude = {long}")

        folium.Marker([lat, long], popup='Current Location').add_to(obj)

        # Ensure output directory exists
        output_dir = "C:/screengfg"
        os.makedirs(output_dir, exist_ok=True)

        file_name = os.path.join(output_dir, f"Location_{datetime.date.today()}.html")
        obj.save(file_name)
        return file_name

    except Exception as e:
        print("Error generating map:", e)
        return False

# Main function
if __name__ == "__main__":
    print("--------------- GPS Using Python ---------------\n")

    page = gps_locator()
    if page:
        print("\n✅ Map generated. Opening in browser...")

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(Path(page).as_uri())
            time.sleep(4)  # Wait for 4 seconds to view
            driver.quit()
            print("\n🗺️  Map Closed. Program finished.")
        except Exception as e:
            print("🚫 Failed to open browser:", e)
    else:
        print("❌ Unable to generate location map.")
