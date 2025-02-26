from PIL import Image

def text_to_binary(text):
    """Convert text to binary string."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    """Convert binary string to text."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_message(image_path, message, output_path):
    """Embed a secret message into an image using LSB steganography."""
    img = Image.open(image_path)
    img = img.convert("RGB")  # Ensure it's in RGB mode
    binary_message = text_to_binary(message) + '1111111111111110'  # End delimiter
    pixels = list(img.getdata())

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message is too long to be hidden in this image.")

    new_pixels = []
    binary_index = 0

    for pixel in pixels:
        new_pixel = list(pixel)
        for i in range(3):  # Modify R, G, B values
            if binary_index < len(binary_message):
                new_pixel[i] = (new_pixel[i] & ~1) | int(binary_message[binary_index])
                binary_index += 1
        new_pixels.append(tuple(new_pixel))

    img.putdata(new_pixels)
    img.save(output_path)
    print(f"✅ Stego-image saved at: {output_path}")

def extract_message(image_path):
    """Extract the hidden message from an image."""
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = list(img.getdata())

    binary_message = ''
    for pixel in pixels:
        for i in range(3):  # Extract LSB from R, G, B
            binary_message += str(pixel[i] & 1)
            if binary_message.endswith('1111111111111110'):  # Stop at delimiter
                return binary_to_text(binary_message[:-16])

    return "❌ No hidden message found."

# File paths
input_image_path = "prettywoman.jpeg"  # Input image
output_image_path = "stego_image.png"  # Output image with hidden text
secret_message = "Hi, this is extremely confidential!!!!"  # Secret message

# Encode the message
hide_message(input_image_path, secret_message, output_image_path)

# Decode the message (for verification)
extracted_message = extract_message(output_image_path)
print(f"🔍 Extracted Message: {extracted_message}")
