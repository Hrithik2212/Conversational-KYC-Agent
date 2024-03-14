import base64


def image_to_base64(image_path, output_path):
    """
    Convert an image file to base64 representation and save it to a text file.

    Args:
        image_path (str): Path to the image file.
        output_path (str): Path to save the base64 string.
    """
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    with open(output_path, "w") as output_file:
        output_file.write(base64_image)
# Example usage
image_path = "full_face.jpg"
base64_image = image_to_base64(image_path , "img.txt")

