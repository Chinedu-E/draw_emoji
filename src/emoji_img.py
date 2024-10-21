import random
from PIL import Image, ImageDraw, ImageFont
from src.bezier import bezier_quadratic
from src.pen import get_glyph_curves


def create_emoji_filled_letter(
    instructions, 
    emojis, 
    width=600, 
    height=750, 
    emoji_size=30, 
    emoji_font_path="fonts/NotoEmoji-VariableFont_wght.ttf") -> Image:
    
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    
    path = []
    for instruction in instructions:
        if instruction[0] == 'moveTo':
            path.append((instruction[1][0], instruction[1][1]))  # Adjusted scaling
        elif instruction[0] == 'lineTo':
            path.append((instruction[1][0], instruction[1][1]))
        elif instruction[0] == 'qCurveTo':
            # Generate Bézier points
            control_points = [
                path[-1],  # Start from the last point in the path
                (instruction[1][0], instruction[1][1] ),
                (instruction[2][0], instruction[2][1])
            ]
            bezier_points_list = bezier_quadratic(control_points, 100)
            path.extend(bezier_points_list)
    draw.line(path, fill='black', width=1)

    # Create a mask for the letter
    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.polygon(path, fill=255)

    emoji_font = ImageFont.truetype(emoji_font_path, emoji_size)

    # Fill the letter with emojis
    for x in range(0, width, emoji_size):
        for y in range(0, height, emoji_size):
            if mask.getpixel((x, y)) > 0:
                emoji = random.choice(emojis)
                draw.text((x, y), emoji, font=emoji_font, fill=random.choice(['red', 'blue', 'green', 'purple', 'orange']))
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    return img


def merge_images(images: list) -> Image:
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    return new_im


def get_emoji_image(text: str, emoji: str, font_path: str="fonts/GeistMonoVF.woff") -> Image:
    glyph_curves = get_glyph_curves(font_path, text)
    images = []
    for instructions in glyph_curves:
        img = create_emoji_filled_letter(instructions, [emoji])
        images.append(img)
    image = merge_images(images)
    return image