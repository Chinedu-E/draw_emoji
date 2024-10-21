# Emoji Art Generator
This project is an emoji-based text art generator that takes user input and converts it into letter shapes filled with emojis. It includes both a Streamlit-based GUI and a script for generating images programmatically.

## Project Structure
```bash
├── fonts            # Emoji font files
├── src/             # Source files for emoji generation and curve drawing
│   ├── bezier.py    # Bézier curve logic
│   ├── draw.py      # Drawing functions for glyphs
│   ├── pen.py       # Pen tools for drawing paths
│   ├── main.py      # Main image generation script
│   ├── emoji_text.py# Converts text to emoji-filled letters
│   └── emoji_img.py # Converts images to emoji-filled shapes
├── app.py           # Streamlit GUI for user input
└── requirements.txt # Python dependencies
```

## Bézier Curves and Glyphs
Bézier curves are used to form the smooth letter outlines. Each curve is controlled by:
- Start Point: The beginning of the curve.
- Control Points: Intermediate points that tweak the curvature.
- End Point: The end of the curve.

The curve can be modified by adjusting the control points, allowing for smoother or sharper bends.

Example of quadratic Bézier curve points:
```python
def bezier_quadratic(control_points, num_points=100):
    """Generates points along a quadratic Bézier curve."""
```

## Running the App
1. Install dependencies (in a venv):
  ```bash
  pip install -r requirements.txt
  ```
2. Run the Streamlit app for interactive usage:
  ```bash
  streamlit run app.py
  ```
3. Generate an image/text:
  ```bash
  python -m src.main
  ```


