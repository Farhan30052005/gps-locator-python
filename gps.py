# Importing Necessary Modules
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import folium
import datetime
import time
import os

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
    except:
        print("Internet Not Available")
        exit()

# This method fetches coordinates and creates an HTML map file
def gps_locator():
    # Create initial map with zoomed out view
    obj = folium.Map(location=[0, 0], zoom_start=2)

    try:
        lat, long, city, state = locationCoordinates()
        print(f"You are in {city}, {state}")
        print(f"Your latitude = {lat} and longitude = {long}")
        folium.Marker([lat, long], popup='Current Location').add_to(obj)

        # Make sure the directory exists
        output_dir = "C:/screengfg"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        fileName = os.path.join(output_dir, f"Location{datetime.date.today()}.html")
        obj.save(fileName)
        return fileName

    except Exception as e:
        print("Error:", e)
        return False

# Main method
if __name__ == "__main__":
    print("--------------- GPS Using Python ---------------\n")

    # Function Calling
    page = gps_locator()
    if page:
        print("\nOpening File.............")
        # Open the generated HTML map in Chrome using Selenium
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("file:///" + page)
        time.sleep(4)
        driver.quit()
        print("\nBrowser Closed..............")
    else:
        print("Unable to generate location map.") 