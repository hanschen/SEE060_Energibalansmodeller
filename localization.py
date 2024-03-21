"""Module for handling localization (translation)."""

from conf import DEBUG, LANG

LANG_SV = {
    # Titles
    "Simplest model": "Enklaste modellen",
    "With greenhouse effect": "Med växthuseffekt",
    "With greenhouse effect and solar absorption": "Med växthuseffekt och absorption av solstrålning",  # noqa
    # Descriptions
    "Surface temperature": "Markens temperatur",
    "Atmospheric temperature": "Atmosfärens temperatur",
    # Sliders descriptions
    "Temperature": "Temperatur",
    "Solar intensity": "Solens intensitet",
    "Planet albedo": "Planetens albedo",
    "Infrared emissivity": "Infraröd emissivitet",
    "Optical absorptivity": "Optisk absorptionsförmåga",
    # Sliders units
    "°C": "°C",
    "% of present value": "% av dagens värde",
    "(fraction)": "(andel)",
}


TRANSLATIONS = {
    "en": None,
    "sv": LANG_SV,
}


def localize(string):
    """Attempt to localize (translate) ``string``.

    If it for some reason fails, the function will raise an exception if debug mode is
    enabled in conf.py, otherwise it will simply return the original string.
    """
    try:
        translation = TRANSLATIONS[LANG]
    except Exception:
        if DEBUG:
            raise
        else:
            return string

    if translation is None:
        return string

    try:
        return translation[string]
    except Exception:
        if DEBUG:
            raise
        else:
            return string
