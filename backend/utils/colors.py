"""Team colors and color utilities for F1 teams."""

# F1 2024 Team Colors (RGB format)
TEAM_COLORS = {
    "Red Bull Racing": "#3671C6",
    "Ferrari": "#E8002D",
    "Mercedes": "#27F4D2",
    "McLaren": "#FF8000",
    "Aston Martin": "#229971",
    "Alpine": "#FF87BC",
    "Williams": "#64C4FF",
    "RB": "#6692FF",
    "Kick Sauber": "#52E252",
    "Haas F1 Team": "#B6BABD",
}

# Tyre compound colors
TYRE_COLORS = {
    "SOFT": "#FF0000",
    "MEDIUM": "#FFD700",
    "HARD": "#FFFFFF",
    "INTERMEDIATE": "#00FF00",
    "WET": "#0000FF",
}

# Status colors
STATUS_COLORS = {
    "active": "#00FF00",
    "retired": "#FF0000",
    "dnf": "#FF0000",
    "dns": "#808080",
}

# UI colors
UI_COLORS = {
    "background": "#1A1A1A",
    "panel": "#2A2A2A",
    "text": "#FFFFFF",
    "text_secondary": "#AAAAAA",
    "border": "#444444",
    "highlight": "#FFD700",
    "track": "#333333",
    "track_outline": "#555555",
}


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple) -> str:
    """Convert RGB tuple to hex color."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def get_team_color(team_name: str) -> str:
    """Get team color by team name."""
    return TEAM_COLORS.get(team_name, "#FFFFFF")


def get_tyre_color(compound: str) -> str:
    """Get tyre color by compound name."""
    return TYRE_COLORS.get(compound.upper(), "#FFFFFF")
