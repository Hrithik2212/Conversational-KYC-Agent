from pdf2image import convert_from_path

def pdf_to_image(pdf_path, output_path, dpi=200):
    """
    Convert a PDF file to an image.

    Args:
        pdf_path (str): Path to the PDF file.
        output_path (str): Path to save the output image.
        dpi (int, optional): Resolution of the output image in dots per inch (DPI). Defaults to 200.
    """
    # Convert PDF to image
    images = convert_from_path(pdf_path, dpi=dpi)

    # Save images
    for i, image in enumerate(images):
        image.save(f"{output_path}_{i+1}.jpg", "JPEG")

# Example usage
pdf_to_image("aadhar.pdf", "aadhar")
pdf_to_image("pan.pdf" , "pan")
