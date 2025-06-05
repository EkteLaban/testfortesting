from PIL import Image, ImageDraw, ImageFont
import json



def create_image_from_bbox_data(json_data, output_filename="rendered_map.png"):
    """
    Generates an image from JSON data containing text elements and their bounding box information.

    Args:
        json_data (dict): A dictionary parsed from the JSON file, expected to have
                          'pages' key with a list of page dictionaries. Each page
                          should have 'page_width', 'page_height', and 'text_elements'.
                          Each text_element should have 'text' and 'bbox'.
        output_filename (str): The name of the file to save the generated image.

    Returns:
        PIL.Image.Image: The generated Pillow Image object.
                         Returns None if the input data format is unexpected.
    """
    if not isinstance(json_data, dict) or 'pages' not in json_data:
        print("Error: Invalid JSON data format. 'pages' key not found.")
        return None

    if not json_data['pages']:
        print("Error: No pages found in the JSON data.")
        return None

    # Assuming we are working with the first page for this example
    page_data = json_data['pages'][0]

    page_width = page_data.get('page_width')
    page_height = page_data.get('page_height')
    text_elements = page_data.get('text_elements', [])

    if page_width is None or page_height is None:
        print("Error: 'page_width' or 'page_height' not found in page data.")
        return None

    # Create a blank image with a white background
    image = Image.new('RGB', (page_width, page_height), 'white')
    draw = ImageDraw.Draw(image)

    # Define a default font. You might need to adjust this based on available fonts
    # or specify a path to a .ttf file if a specific font is required.
    try:
        # Attempt to load a common sans-serif font like Arial
        font = ImageFont.truetype("arial.ttf", 10)
    except IOError:
        # Fallback to a default Pillow font if Arial is not found
        print("Warning: Arial font not found. Using default Pillow font. Text appearance may vary.")
        font = ImageFont.load_default()

    # Draw each text element on the image
    for element in text_elements:
        text = element.get('text')
        bbox = element.get('bbox') # [x, y, width, height]

        if text is None or bbox is None or len(bbox) != 4:
            print(f"Warning: Skipping malformed text element: {element}")
            continue

        x, y, width, height = bbox

        # You might want to adjust the font size based on the bbox height
        # For simplicity, we're using a fixed font size here.
        # If you need to fit text perfectly, you'd calculate font size based on height.

        draw.text((x, y), text, fill='black', font=font)

    # Save the image to the specified filename
    image.save(output_filename)
    print(f"Image '{output_filename}' created successfully.")

    return image
