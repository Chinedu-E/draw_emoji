from PIL import Image, ImageDraw
from src.bezier import bezier_quadratic
from src.pen import get_glyph_curves



def create_emoji_filled_letter_text(instructions: list, emoji: str, scale_factor=85, width=8, height=8) -> str:
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    path = []
    for instruction in instructions:
        if instruction[0] == 'moveTo':
            path.append((instruction[1][0] / scale_factor, instruction[1][1] / scale_factor))
        elif instruction[0] == 'lineTo':
            path.append((instruction[1][0] / scale_factor, instruction[1][1] / scale_factor))
        elif instruction[0] == 'qCurveTo':
            # Generate Bézier points
            control_points = [
                path[-1],  # Start from the last point in the path
                (instruction[1][0] / scale_factor, instruction[1][1] / scale_factor),
                (instruction[2][0] / scale_factor, instruction[2][1] / scale_factor)
            ]
            bezier_points_list = bezier_quadratic(control_points, 250)
            path.extend(bezier_points_list)
            
    draw.line(path, fill='black', width=1)
    
    # Create a mask for the letter
    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.polygon(path, fill=255)
    
    # Fill the letter with emojis
    for y in range(height):
        for x in range(width):
            if mask.getpixel((x, y)) > 0:
                grid[y][x] = emoji
                
    return '\n'.join(''.join(row) for row in reversed(grid))


def get_emoji_text(text: str, emoji: str, font_path="GeistMonoVF.woff") -> list[str]:
    glyph_curves = get_glyph_curves(font_path, text)
    result = [create_emoji_filled_letter_text(instructions, emoji) for instructions in glyph_curves]
    return result