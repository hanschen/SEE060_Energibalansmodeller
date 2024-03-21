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

    sfc_temp_K = (
        (solar_intensity * (1 - planet_albedo))
        / (sigma * (4 - 2 * infrared_emissivity))
    ) ** (1 / 4)

    atm_temp_K = (
        (solar_intensity * (1 - planet_albedo))
        / (sigma * (8 - 4 * infrared_emissivity))
    ) ** (1 / 4)

    sfc_temp_C = sfc_temp_K + constants.ABSOLUTE_ZERO_DEG_C
    atm_temp_C = atm_temp_K + constants.ABSOLUTE_ZERO_DEG_C

    temperatures = {
        "Surface temperature": sfc_temp_C,
        "Atmospheric temperature": atm_temp_C,
    }

    return temperatures


temperatures = radiation_model_greenhouse_effect(
    solar_intensity_percent=100.0, planet_albedo=0.3, infrared_emissivity=0.9
)

utils.draw_thermometers(
    temperatures,
    radiation_model=radiation_model_greenhouse_effect,
    variables=["solar", "albedo", "emissivity"],
)
