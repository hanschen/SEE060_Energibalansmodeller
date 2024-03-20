from ipywidgets import interact

import constants
import utils


def radiation_model_simplest(solar_intensity_percent, planet_albedo):
    """Simplest version of the energy balance model of the Earth.

    Considers only solar intensity and the planet's surface albedo.

    Returns the surface temperature in degree Celsius.
    """
    solar_intensity = solar_intensity_percent / 100 * constants.SOLAR_INTENSITY
    sigma = constants.STEFAN_BOLTZMANN_CONSTANT
    sfc_temp = ((solar_intensity * (1 - planet_albedo)) / (4 * sigma)) ** (1 / 4)
    return sfc_temp


sliders = utils.create_sliders(["solar", "albedo"])


@interact(**sliders)
def draw(solar_intensity_percent, planet_albedo):
    sfc_temp_K = radiation_model_simplest(solar_intensity_percent, planet_albedo)
    sfc_temp_C = sfc_temp_K + constants.ABSOLUTE_ZERO_DEG_C
    temperatures = {"Surface temperature": sfc_temp_C}
    utils.draw_thermometers(temperatures, title="Simplest model")
