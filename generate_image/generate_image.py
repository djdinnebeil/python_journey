import json
import os
import openai
import dotenv
import requests

dotenv.load_dotenv()

def generate_image(prompt, model="gpt-image-1", num_images=1, size="1024x1024", response_format="url"):
    # Load the API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "n": num_images,
        "size": size,
        # "response_format": response_format
    }

    url = "https://api.openai.com/v1/images/generations"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()

        # Check for errors in the response
        if response.status_code != 200:
            print(f"Error: {data.get('error', {}).get('message', 'Unknown error')}")
            return None

        # Extract URLs or base64 images depending on the response format
        if response_format == "url":
            image_urls = [img['url'] for img in data['data']]
            return image_urls
        elif response_format == "b64_json":
            image_data = [img['b64_json'] for img in data['data']]
            return image_data

    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def save_image_from_url(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as {filename}")
    except Exception as e:
        print(f"Error saving image: {e}")

if __name__ == "__main__":
    # Example usage
    prompt = "A cute baby sea otter"
    images = generate_image(prompt, model="gpt-image-1", num_images=1, size="1024x1024", response_format="url")

    if images:
        for idx, url in enumerate(images):
            print(f"Image {idx + 1}: {url}")
            save_image_from_url(url, f"generated_image_{idx+1}.png")
