from ipywidgets import interact

import constants
import utils


def radiation_model_greenhouse_effect_and_solar_absorption(
    solar_intensity_percent, planet_albedo, infrared_emissivity, optical_absorptivity
):
    """Energy balance model of the Earth that includes the greenhouse effect and solar
    absorption in the atmosphere.

    Returns the surface and atmospheric temperatures in degree Celsius.
    """
    solar_intensity = solar_intensity_percent / 100 * constants.SOLAR_INTENSITY
    sigma = constants.STEFAN_BOLTZMANN_CONSTANT

    # A_prime is the fraction of absorbed solar radiation at the surface
    A_prime = (1 - optical_absorptivity) * (1 - planet_albedo)

    # A_e is the fraction of solar radiation that is reflected back to space at the top
    # of the atmosphere
    A_e = (1 - optical_absorptivity) ** 2 * planet_albedo

    sfc_temp = (
        (solar_intensity * (1 - A_e + A_prime))
        / (4 * sigma * (2 - infrared_emissivity))
    ) ** (1 / 4)
    atm_temp = (
        (4 * sigma * sfc_temp**4 - solar_intensity * A_prime)
        / (4 * infrared_emissivity * sigma)
    ) ** (1 / 4)
    return sfc_temp, atm_temp


sliders = utils.create_sliders(["solar", "albedo", "emissivity", "absorptivity"])


@interact(**sliders)
def draw(
    solar_intensity_percent, planet_albedo, infrared_emissivity, optical_absorptivity
):
    sfc_temp_K, atm_temp_K = radiation_model_greenhouse_effect_and_solar_absorption(
        solar_intensity_percent,
        planet_albedo,
        infrared_emissivity,
        optical_absorptivity,
    )
    sfc_temp_C = sfc_temp_K + constants.ABSOLUTE_ZERO_DEG_C
    atm_temp_C = atm_temp_K + constants.ABSOLUTE_ZERO_DEG_C
    temperatures = {
        "Surface temperature": sfc_temp_C,
        "Atmospheric temperature": atm_temp_C,
    }
    utils.draw_thermometers(
        temperatures, title="With greenhouse effect and solar absorption"
    )
