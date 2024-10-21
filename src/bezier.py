from PIL import ImageDraw

def bezier_points(instructions, num_points=100):
    """Calculate points on a Bézier curve based on drawing instructions."""
    points = []
    current_point = None
    
    for cmd, *args in instructions:
        if cmd == 'moveTo':
            current_point = args[0]
            points.append(current_point)
        elif cmd == 'lineTo':
            current_point = args[0]
            points.append(current_point)
        elif cmd == 'qCurveTo':
            control_points = [current_point] + list(args)
            bezier_curve_points = bezier_quadratic(control_points, num_points)
            points.extend(bezier_curve_points)
            current_point = control_points[-1]  # Set the current point to the last point in the curve
        elif cmd == 'closePath':
            # Close path logic if needed
            pass
            
    return points

def bezier_quadratic(control_points, num_points):
    """Calculate quadratic Bézier curve points."""
    return [
        (
            (1 - t) ** 2 * control_points[0][0] +
            2 * (1 - t) * t * control_points[1][0] +
            t ** 2 * control_points[2][0],
            (1 - t) ** 2 * control_points[0][1] +
            2 * (1 - t) * t * control_points[1][1] +
            t ** 2 * control_points[2][1]
        )
        for t in (i / (num_points - 1) for i in range(num_points))
    ]

