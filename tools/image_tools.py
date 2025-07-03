# # image_tools.py

# from PIL import Image
# import os

# def load_image(image_path):
#     """Load an image from the specified path."""
#     if not os.path.exists(image_path):
#         raise FileNotFoundError(f"No image found at {image_path}")
#     return Image.open(image_path)

# def save_image(image, save_path):
#     """Save the image to the specified path."""
#     image.save(save_path)

# def resize_image(image, size):
#     """Resize the image to the specified size."""
#     return image.resize(size)

# def crop_image(image, box):
#     """Crop the image to the specified box (left, upper, right, lower)."""
#     return image.crop(box)

# def show_image(image):
#     """Display the image."""
#     image.show()