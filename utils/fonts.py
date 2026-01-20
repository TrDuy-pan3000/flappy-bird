import pygame
import os

# Font helper for Vietnamese Unicode support
# Pygame's default font doesn't support Vietnamese characters
# We need to use system fonts that support Unicode

_font_cache = {}

def get_vietnamese_font(size):
    """Get a font that supports Vietnamese characters"""
    if size in _font_cache:
        return _font_cache[size]
    
    # List of fallback fonts that support Vietnamese
    vietnamese_fonts = [
        "segoeuiemoji",  # Windows - has emoji + unicode
        "segoeui",       # Windows Segoe UI
        "arial",         # Common fallback
        "arialunicode",  # Arial Unicode MS
        "tahoma",        # Tahoma
        "msyh",          # Microsoft YaHei
        "noto",          # Noto Sans (if installed)
        "dejavusans",    # DejaVu Sans
        None             # Pygame default as last resort
    ]
    
    font = None
    for font_name in vietnamese_fonts:
        try:
            if font_name:
                font = pygame.font.SysFont(font_name, size)
                # Test if font can render Vietnamese
                test_surf = font.render("Xin Chào", True, (255, 255, 255))
                if test_surf.get_width() > 10:
                    _font_cache[size] = font
                    return font
            else:
                font = pygame.font.Font(None, size)
                _font_cache[size] = font
                return font
        except:
            continue
    
    # Fallback to default
    font = pygame.font.Font(None, size)
    _font_cache[size] = font
    return font


def get_font(size, bold=False):
    """Get a font, preferring Vietnamese-compatible fonts"""
    return get_vietnamese_font(size)


class VietnameseFont:
    """Font wrapper that handles Vietnamese text properly"""
    
    def __init__(self, size):
        self.size = size
        self._font = None
        
    @property
    def font(self):
        if self._font is None:
            self._font = get_vietnamese_font(self.size)
        return self._font
    
    def render(self, text, antialias, color, background=None):
        """Render text with Vietnamese support"""
        return self.font.render(text, antialias, color, background)
    
    def size_text(self, text):
        """Get size of rendered text"""
        return self.font.size(text)
    
    def get_height(self):
        return self.font.get_height()
    
    def get_linesize(self):
        return self.font.get_linesize()
