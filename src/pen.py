import traceback
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen


class GlyphPen(BasePen):
    """Pen to collect glyph outlines as Bézier curves or lines."""

    def __init__(self, glyph_set):
        super().__init__(glyph_set)
        self.path = []

    def _moveTo(self, pt):
        """Start a new subpath at pt."""
        self.path.append(("moveTo", pt))

    def _lineTo(self, pt):
        """Draw a line to pt."""
        self.path.append(("lineTo", pt))

    def _curveToOne(self, pt1, pt2, pt3):
        """Draw a cubic Bézier curve."""
        self.path.append(("curveTo", pt1, pt2, pt3))

    def _qCurveToOne(self, pt1, pt2):
        """Draw a quadratic Bézier curve."""
        self.path.append(("qCurveTo", pt1, pt2))

    def _closePath(self):
        """Close the current path."""
        self.path.append(("closePath",))



def get_glyph_curves(font_path, text):
    """Extract glyph curves from the font for the given text."""
    font = TTFont(font_path)
    glyph_set = font.getGlyphSet()
    glyph_curves = []

    for char in text:
        if char == " ":
            continue
        try:
            glyph = glyph_set[char]
            pen = GlyphPen(glyph_set)
            glyph.draw(pen)
            glyph_curves.append(pen.path)
        except Exception as e:
            print(traceback.format_exc())

    return glyph_curves