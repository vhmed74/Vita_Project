import os
import requests
from duckduckgo_search import DDGS

# Define the queries for components
components = {
    "arduino": "Arduino UNO R3 board white background isolated",
    "esp32": "ESP32 development board white background",
    "dht22": "DHT22 temperature humidity sensor white background",
    "ds18b20": "DS18B20 waterproof temperature sensor probe white background",
    "mq135": "MQ135 gas sensor module white background",
    "lm386": "LM386 sound sensor module white background",
    "hx711": "HX711 load cell amplifier module white background",
    "loadcell": "aluminum load cell weight sensor white background",
    "ssr": "Solid state relay module arduino white background"
}

output_dir = r"C:\Users\LOQ\Downloads\Smart_Incubator_Presentation\images"

def download_image(name, query):
    try:
        ddgs = DDGS()
        results = ddgs.images(query, max_results=3)
        if not results:
            print(f"No results for {name}")
            return
        
        # Try to download the first valid image
        for result in results:
            url = result['image']
            try:
                img_data = requests.get(url, timeout=5).content
                with open(os.path.join(output_dir, f"{name}.png"), "wb") as f:
                    f.write(img_data)
                print(f"Successfully downloaded {name}.png")
                return
            except Exception as e:
                print(f"Failed to download {url}: {e}")
                continue
    except Exception as e:
        print(f"Search failed for {name}: {e}")

if __name__ == "__main__":
    for name, query in components.items():
        download_image(name, query)
