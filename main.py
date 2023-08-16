# Import necessary modules
import os

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from google.cloud import storage

# Define the program constants
BUCKET_NAME = "<YOUR-BUCKET-NAME>"
TEMPLATE_CERTIFICATE_NAME = "template_certificate.png"
MAIN_FONT_NAME = "proxima-nova-black.otf"
SECONDARY_FOND_NAME = "open-sans-regular.ttf"
POINT_SIZE = int(96/72)
TEXT_COLOR_RGB = (0, 0, 0)


# Define the function that generate the certificate
def generate_certificate(request):
    """
    This function add the specified data to the template of the certificate and return it as a custom certificate
    :param request: take from URL the variables values for:
    student_name: the name of the student for whom the certificate is generated
    title: the name of the Retraining Program for which the certificate is generated
    status: specifies whether a student has finished a program successfully
    date: specifies the date of completion
    :return: return the generated certificate in browser
    """
    # Retrieve the values of the required parameters and format them
    request_json = request.get_json()
    if request.args and 'student_name' and 'title' and 'status' and 'date' in request.args:
        student_name = request.args.get('student_name').title()
        title = request.args.get('title').upper()
        status = "has " + request.args.get('status').lower()
        date = request.args.get('date')
    elif request_json and 'student_name' and 'title' and 'status' and 'date' in request_json:
        student_name = request_json['student_name'].title()
        title = request_json['title'].upper()
        status = "has " + request_json['status'].lower()
        date = request_json['date']
    else:
        student_name = ""
        title = ""
        status = ""
        date = ""

    # Download the template image from the storage bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(TEMPLATE_CERTIFICATE_NAME)
    image_bytes = blob.download_as_bytes()

    # Download the font files to a temporary directory
    main_font_blob = bucket.blob(MAIN_FONT_NAME)
    second_font_blob = bucket.blob(SECONDARY_FOND_NAME)
    main_font_file_path = os.path.join('/tmp', MAIN_FONT_NAME)
    second_font_file_path = os.path.join('/tmp', SECONDARY_FOND_NAME)
    main_font_blob.download_to_filename(main_font_file_path)
    second_font_blob.download_to_filename(second_font_file_path)

    # Load template image into Pillow
    image = Image.open(BytesIO(image_bytes))

    # Create a drawing canvas overlay on top of the image
    draw = ImageDraw.Draw(image)

    # Define the font and the size for each text area
    student_name_font = ImageFont.truetype(main_font_file_path, 24 * POINT_SIZE)
    title_font = ImageFont.truetype(main_font_file_path, 24 * POINT_SIZE)
    status_font = ImageFont.truetype(second_font_file_path, 18 * POINT_SIZE)
    date_font = ImageFont.truetype(second_font_file_path, 12 * POINT_SIZE)

    # Get size of texts
    name_text_width, _ = draw.textsize(student_name, font=student_name_font)
    title_text_width, _ = draw.textsize(title, font=title_font)
    status_text_width, _ = draw.textsize(status, font=status_font)

    # Calculate central position of texts
    image_width, _ = image.size
    name_text_x = (image_width - name_text_width) // 2
    title_text_x = (image_width - title_text_width) // 2
    status_text_x = (image_width - status_text_width) // 2

    # Add the texts to the certificate
    draw.text((name_text_x, 275), student_name, font=student_name_font, fill=TEXT_COLOR_RGB)
    draw.text((title_text_x, 343), title, font=title_font, fill=TEXT_COLOR_RGB)
    draw.text((status_text_x, 311), status, font=status_font, fill=TEXT_COLOR_RGB)
    draw.text((745, 533), date, font=date_font, fill=TEXT_COLOR_RGB)

    # Convert Pillow image back to bytes
    with BytesIO() as output:
        image.save(output, format='PNG')
        generated_certificate = output.getvalue()

    # Return the completed certificate in browser
    headers = {'Content-Type': 'image/png'}
    return generated_certificate, 200, headers
