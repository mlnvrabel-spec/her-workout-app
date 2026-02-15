
import io
import base64
from PIL import Image

def process_and_split_image(image_path):
    # Load the generated image
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    
    # Split into left (Front) and right (Back) halves
    # Assuming side-by-side generation. If top-bottom or centred, we adjust.
    # The prompt asked for "front view and back view side by side"
    
    # Let's verify the content by just processing the whole thing first?
    # No, we need separate images for the HTML structure which has distinct .body-view divs
    
    # Crop halves
    front_img = img.crop((0, 0, width // 2, height))
    back_img = img.crop((width // 2, 0, width, height))
    
    # Function to remove black background and trim
    def clean_image(image):
        datas = image.getdata()
        new_data = []
        for item in datas:
            # Threshold for black/dark grey transparency
            # Being very aggressive to remove all background
            if item[0] < 80 and item[1] < 80 and item[2] < 80:
                new_data.append((0, 0, 0, 0))
            else:
                # Keep original pixel
                new_data.append(item)
        
        image.putdata(new_data)
        
        # Trim transparent borders
        bbox = image.getbbox()
        if bbox:
            image = image.crop(bbox)
            
        return image

    front_cleaned = clean_image(front_img)
    back_cleaned = clean_image(back_img)
    
    # Convert to base64
    def to_base64(image):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
        
    front_b64 = to_base64(front_cleaned)
    back_b64 = to_base64(back_cleaned)
    
    return front_b64, back_b64

def update_html(html_path, image_path):
    front_b64, back_b64 = process_and_split_image(image_path)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We need to replace the TWO base64 images in the file.
    # The first one is Front View, the second is Back View.
    # We can use regex to find them sequentially.
    
    import re
    # Pattern for data:image/png;base64,....."
    # We look for the href attribute
    
    parts = re.split(r'(href="data:image/[^;]+;base64,[^"]+")', content)
    
    # parts[0] is before first img
    # parts[1] is first img tag (Front)
    # parts[2] is between imgs
    # parts[3] is second img tag (Back)
    # parts[4] is rest
    
    if len(parts) >= 5:
        new_front_tag = f'href="data:image/png;base64,{front_b64}"'
        new_back_tag = f'href="data:image/png;base64,{back_b64}"'
        
        new_content = parts[0] + new_front_tag + parts[2] + new_back_tag + parts[4]
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated HTML with new body images.")
    else:
        print("Could not find both image tags to replace.")

if __name__ == "__main__":
    # Path to the generated image - I will need to get this from the previous tool output or passed as arg
    # Hardcoding for the script execution via tool
    import sys
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        html_path = r"c:\Users\mlnvr\Desktop\Antigravity\Workout Split Dashboard\Workout Dashboard.html"
        update_html(html_path, img_path)
    else:
        print("No image path provided")
