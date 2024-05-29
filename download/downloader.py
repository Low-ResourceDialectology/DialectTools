import requests
import os

def download_text_data(urls, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for idx, url in enumerate(urls):
        # Send a GET request to the URL
        response = requests.get(url)
        
        if response.status_code == 200:
            # Get the filename from the URL or generate a default one
            filename = os.path.basename(url) or f"file_{idx}.txt"
            
            # Save the downloaded content to a file in the output directory
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Downloaded: {url} -> {output_path}")
        else:
            print(f"Failed to download {url} with status code: {response.status_code}")

# Example usage
urls = [
    'https://example.com/text1.txt',  # Replace with your URLs
    'https://example.com/text2.txt'
]
output_dir = 'downloaded_text_data'
download_text_data(urls, output_dir)
