from ipywidgets import interact

import constants
import utils


def radiation_model_greenhouse_effect(
    solar_intensity_percent, planet_albedo, infrared_emissivity
):
    """Energy balance model of the Earth that includes the greenhouse effect.

    Returns the surface and atmospheric temperatures in degree Celsius.
    """
    solar_intensity = solar_intensity_percent / 100 * constants.SOLAR_INTENSITY
    sigma = constants.STEFAN_BOLTZMANN_CONSTANT

    sfc_temp = (
        (solar_intensity * (1 - planet_albedo))
        / (sigma * (4 - 2 * infrared_emissivity))
    ) ** (1 / 4)

    atm_temp = (
        (solar_intensity * (1 - planet_albedo))
        / (sigma * (8 - 4 * infrared_emissivity))
    ) ** (1 / 4)

    return sfc_temp, atm_temp


sliders = utils.create_sliders(["solar", "albedo", "emissivity"])


@interact(**sliders)
def draw(solar_intensity_percent, planet_albedo, infrared_emissivity):
    sfc_temp_K, atm_temp_K = radiation_model_greenhouse_effect(
        solar_intensity_percent, planet_albedo, infrared_emissivity
    )
    sfc_temp_C = sfc_temp_K + constants.ABSOLUTE_ZERO_DEG_C
    atm_temp_C = atm_temp_K + constants.ABSOLUTE_ZERO_DEG_C
    temperatures = {
        "Surface temperature": sfc_temp_C,
        "Atmospheric temperature": atm_temp_C,
    }
    utils.draw_thermometers(temperatures, title="With greenhouse effect")
