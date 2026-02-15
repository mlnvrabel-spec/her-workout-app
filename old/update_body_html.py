import re

html_path = r'c:\Users\mlnvr\Desktop\Antigravity\Workout Split Dashboard\Workout Dashboard.html'

try:
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Path data generated from generate_body_path.py
    path_data = "M 50 5 L 42 8 L 40 18 L 42 26 L 35 28 L 20 30 L 10 38 L 8 55 L 8 75 L 6 85 L 4 90 L 8 95 L 12 90 L 14 85 L 16 60 L 20 50 L 25 60 L 28 80 L 26 90 L 24 110 L 24 140 L 26 160 L 28 172 L 26 178 L 35 178 L 40 175 L 40 160 L 42 140 L 44 110 L 48 95 L 52 95 L 56 110 L 58 140 L 60 160 L 60 175 L 65 178 L 74 178 L 72 172 L 74 160 L 76 140 L 76 110 L 74 90 L 72 80 L 75 60 L 80 50 L 84 60 L 86 85 L 88 90 L 92 95 L 96 90 L 94 85 L 92 75 L 92 55 L 90 38 L 80 30 L 65 28 L 58 26 L 60 18 L 58 8 Z"

    # New SVG Element
    new_tag = f'<path d="{path_data}" class="body-silhouette" />'

    # Regex to find the <image> tag with base64 content
    # Matches <image ... href="data:image/png;base64,..." ... /> including multi-line
    pattern = r'<image\s+[^>]*href="data:image/png;base64,[^"]+"[^>]*/>'
    
    # Check identifying matches first
    matches = re.findall(pattern, content, flags=re.DOTALL)
    print(f"Found {len(matches)} image tags to replace.")

    if len(matches) > 0:
        new_content = re.sub(pattern, new_tag, content, flags=re.DOTALL)
        
        # Add CSS if not present
        if ".body-silhouette" not in new_content:
            css_marker = "/* Mask styling (covering the image) */"
            css_insert = """
        /* Body Silhouette Base */
        .body-silhouette {
            fill: #1a1a1a;
            stroke: #333;
            stroke-width: 0.5px;
        }

        """
            if css_marker in new_content:
                new_content = new_content.replace(css_marker, css_insert + css_marker)
                print("Added CSS for body-silhouette.")
            else:
                print("Could not find CSS marker to insert styles.")
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated HTML with SVG silhouette.")
    else:
        print("No matching image tags found. Content might not match regex.")

except Exception as e:
    print(f"Error: {e}")
