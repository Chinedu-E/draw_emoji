import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from PIL import Image, ImageDraw

from src.bezier import bezier_points, bezier_quadratic

def draw_shape_matplotlib(instructions):
    # Convert instructions to vertices and codes
    verts = []
    codes = []
    for cmd, *args in instructions:
        if cmd == 'moveTo':
            verts.append(args[0])
            codes.append(Path.MOVETO)
        elif cmd == 'lineTo':
            verts.append(args[0])
            codes.append(Path.LINETO)
        elif cmd == 'curveTo':
            # Add control points for cubic curves
            verts.extend(args)  # args should contain three points for cubic
            codes.extend([Path.CURVE4] * 3)  # Add curve points with CURVE4
        elif cmd == 'qCurveTo':
            # Add control points for quadratic curves
            verts.extend(args)  # args should contain two points for quadratic
            codes.extend([Path.CURVE3] * 2)  # Add curve points with CURVE3
        elif cmd == 'closePath':
            codes.append(Path.CLOSEPOLY)
            verts.append(verts[0])  # Add the first point again to close the path

    # Create the path
    path = Path(verts, codes)

    # Set up the plot
    fig, ax = plt.subplots()
    patch = patches.PathPatch(path, facecolor='none', lw=2)
    ax.add_patch(patch)

    # Set the plot limits
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 800)

    # Invert the y-axis to match the original coordinate system
    ax.invert_yaxis()

    # Remove axes
    ax.axis('off')

    # Save the plot
    plt.savefig('shape_matplotlib.png', dpi=300, bbox_inches='tight')
    print("Image saved as 'shape_matplotlib.png'")


def draw_shape_pillow(instructions):
    # Create a new image with a white background
    width, height = 600, 800
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # List of drawing instructions
    path = []
    for cmd, *args in instructions:
        if cmd in ['moveTo', 'lineTo']:
            path.append(args[0])
        elif cmd == 'curveTo':
            # Handle cubic curves
            p1, p2, p3 = args
            path.append(p1)
            path.append(p2)
            path.append(p3)
            # Use a small number of points to create a curve
            curve_points = bezier_points([path[-4], p1, p2, p3], num_points=20)
            path.extend(curve_points[1:])  # Avoid duplicating the first point
        elif cmd == 'qCurveTo':
            # Handle quadratic curves
            p1, p2 = args
            path.append(p1)
            # Use a small number of points to create a curve
            curve_points = bezier_points([path[-3], p1, p2], num_points=20)
            print(curve_points)
            path.extend(curve_points[1:])  # Avoid duplicating the first point
        elif cmd == 'closePath':
            path.append(path[0])  # Close the path

    # Draw the path
    draw.line(path, fill='black', width=2)

    # Save the image
    image.save('shape_pillow.png')
    print("Image saved as 'shape_pillow.png'")


def place_emojis_on_curve(image, instructions, emoji_text, emoji_font):
    """Place emojis along the curves of glyphs."""
    draw = ImageDraw.Draw(image)

    for cmd, *args in instructions:
        if cmd == 'moveTo':
            current_position = args[0]
        elif cmd == 'qCurveTo':
            control_points = [current_position] + list(args)
            emoji_positions = bezier_quadratic(control_points, num_points=100)
            current_position = control_points[-1]
            for position in emoji_positions:
                draw.text(position, emoji_text, font=emoji_font, fill=(0, 0, 0))
        elif cmd == 'closePath':
            # Handle closing path if needed
            pass