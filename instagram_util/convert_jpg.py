from PIL import Image
import os

def convert_to_jpg(input_file_path):
    try:
        with Image.open(input_file_path) as img:
            # Convert to RGB mode if image mode is not RGB
            if img.mode != "RGB":
                img = img.convert("RGB")
            # Get the output file path by changing the extension to ".jpg"
            output_file_path = os.path.splitext(input_file_path)[0] + ".jpg"
            # Save the image in JPEG format
            os.remove(input_file_path)
            img.save(output_file_path, "JPEG", quality=95)
        return output_file_path
    except IOError:
        raise IOError(f"Error converting {input_file_path} to JPEG")
