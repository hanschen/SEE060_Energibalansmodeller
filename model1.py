import constants
import utils


def radiation_model_simplest(solar_intensity_percent, planet_albedo):
    """Simplest version of the energy balance model of the Earth.

    Considers only solar intensity and the planet's surface albedo.

    Returns the surface temperature in degree Celsius.
    """
    solar_intensity = solar_intensity_percent / 100 * constants.SOLAR_INTENSITY
    sigma = constants.STEFAN_BOLTZMANN_CONSTANT

    sfc_temp_K = ((solar_intensity * (1 - planet_albedo)) / (4 * sigma)) ** (1 / 4)

    sfc_temp_C = sfc_temp_K + constants.ABSOLUTE_ZERO_DEG_C

    temperatures = {"Surface temperature": sfc_temp_C}

    return temperatures


temperatures = radiation_model_simplest(100, 0.3)


utils.draw_thermometers(
    temperatures,
    radiation_model=radiation_model_simplest,
    variables=["solar", "albedo"],
)
