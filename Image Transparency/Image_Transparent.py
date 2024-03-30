from PIL import Image

def adjust_opacity(image_path, output_path, opacity):
    # Open the image
    img = Image.open(image_path)

    # Create a transparent overlay image with the same size as the original image
    overlay = Image.new('RGBA', img.size, (255, 255, 255, int(255 * opacity)))

    # Composite the original image with the overlay using the alpha parameter
    img_with_opacity = Image.alpha_composite(img.convert('RGBA'), overlay)

    # Save the modified image
    img_with_opacity.save(output_path)

# Replace input_image_path with the path to your input image
input_image_path = 'Sample Image.jpg'

# Replace output_image_path with the desired output image path and filename
# Its always going to be saved in png as jpg dosen't support transparent background
# So if image has transparent backgorund it is gonna show error
output_image_path = 'Sample_Image_Transparent.png'

# Adjust the opacity value (0.0 to 1.0)
opacity_value = 0.8  # Example: 0.8 for 80% opacity

# Call the function to adjust opacity and save the image
adjust_opacity(input_image_path, output_image_path, opacity_value)

print("Image with adjusted opacity saved to same location as that of input image.")
