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

    sfc_temp_K = (
        (solar_intensity * (1 - A_e + A_prime))
        / (4 * sigma * (2 - infrared_emissivity))
    ) ** (1 / 4)

    atm_temp_K = (
        (solar_intensity * (1 - A_e - A_prime * (1 - infrared_emissivity)))
        / (4 * infrared_emissivity * sigma * (2 - infrared_emissivity))
    ) ** (1 / 4)

    sfc_temp_C = sfc_temp_K + constants.ABSOLUTE_ZERO_DEG_C
    atm_temp_C = atm_temp_K + constants.ABSOLUTE_ZERO_DEG_C

    temperatures = {
        "Surface temperature": sfc_temp_C,
        "Atmospheric temperature": atm_temp_C,
    }

    return temperatures


temperatures = radiation_model_greenhouse_effect_and_solar_absorption(
    solar_intensity_percent=100,
    planet_albedo=0.3,
    infrared_emissivity=0.9,
    optical_absorptivity=0.105,
)

utils.draw_thermometers(
    temperatures,
    radiation_model=radiation_model_greenhouse_effect_and_solar_absorption,
    variables=["solar", "albedo", "emissivity", "absorptivity"],
    title="With greenhouse effect and solar absorption",
)
