"""Utilities to create sliders and draw thermometers."""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from ipywidgets import widgets

import conf
from localization import localize


def create_sliders(variables):
    """Return a dictionary with some standard slider widgets.

    Parameters
    ----------
    variables : list, {"temperature", "solar", "albedo", "emissivity"}
        A list containing variables to create sliders for.

    """
    layout = widgets.Layout(width="auto", height="auto")
    common_kwargs = dict(
        layout=layout,
        style={"description_width": "initial"},
    )
    sliders = {}

    if "temperature" in variables:
        sliders["temperature"] = widgets.FloatSlider(
            value=20.0,
            min=-273.0,
            max=100.0,
            step=1.0,
            description=localize("Temperature"),
            readout_format=".0f",
            **common_kwargs,
        )

    if "solar" in variables:
        sliders["solar_intensity_percent"] = widgets.FloatSlider(
            value=100.0,
            min=50.0,
            max=150.0,
            step=1.0,
            description=localize("Solar intensity (% of present value)"),
            readout_format=".0f",
            **common_kwargs,
        )

    if "albedo" in variables:
        sliders["planet_albedo"] = widgets.FloatSlider(
            value=0.30,
            min=0.0,
            max=1.0,
            step=0.01,
            description=localize("Planet albedo (fraction)"),
            readout_format=".2f",
            **common_kwargs,
        )

    if "emissivity" in variables:
        sliders["infrared_emissivity"] = widgets.FloatSlider(
            value=0.9,
            min=0.7,
            max=1.0,
            step=0.001,
            description=localize("Infrared emissivity (fraction)"),
            readout_format=".3f",
            **common_kwargs,
        )

    if "absorptivity" in variables:
        sliders["optical_absorptivity"] = widgets.FloatSlider(
            value=0.105,
            min=0.0,
            max=0.5,
            step=0.001,
            description=localize("Optical absorptivity (fraction)"),
            readout_format=".3f",
            **common_kwargs,
        )

    return sliders


def draw_thermometers(temperatures, title=None, colors=None, **kwargs):
    """Draw thermometers for descriptions and temperatures in ``temperatures`` dict.

    The temperatures should be in degrees Celsius.

    Accepts optional title for the figure, list of colors for the thermometers, and
    kwargs passed to the Thermometer class.
    """
    num_thermometers = len(temperatures)

    if colors is None:
        colors = ["r", "b"] * num_thermometers

    fig, axes = plt.subplots(1, num_thermometers)
    if title is not None:
        fig.suptitle(localize(title))

    # Workaround for when there is only one thermometer
    if num_thermometers == 1:
        axes = [axes]

    for i, (description, temperature) in enumerate(temperatures.items()):
        kwargs_current = kwargs.copy()
        kwargs_current["facecolor"] = colors[i]
        thermometer = Thermometer(**kwargs_current)
        thermometer.draw(temperature, ax=axes[i], description=description)


class Thermometer:
    def __init__(
        self,
        min=-273.15,
        max=100.0,
        units=" °C",
        barwidth=40,
        bulbwidth=None,
        linewidth=3.0,
        facecolor="r",
        edgecolor="k",
        padding_x=5.0,
        padding_y=8.0,
    ):
        """Initialize the Thermometer.

        The thermometer consists of a "bar" and a "bulb" at the bottom.

        Note that the unit for all sizes (``barwidth``, ``linewidth``, etc.) are in data
        units, so the same units as the temperature.

        Parameters
        ----------
        min : float
            Min temperature of the thermometer. Default: -273.15.
        max : float
            Max temperature of the thermometer. Default: 100.0.
        units : str
            Units for the temperature. Only affects displayed text and tick labels.
        barwidth : float, optional
            Width of the bar of the thermometer. Default: 40.0.
        bulbwidth : float, optional
            Width (and height) of the bulb. Default: Twice of ``barwidth``.
        linewidth : float, optional
            Width of the line outlining the thermometer. Default: 3.0.
        facecolor : color or None
            Color of temperature fill. Default: "r".
        edgecolor : color or None
            Color of thermometer outline. Default: "k".
        padding_x : float, optional
            Padding around thermometer in the x-direction. Default: 5.0.
        padding_y : float, optional
            Padding around thermometer in the y-direction. Default: 8.0.

        """
        self.min = min
        self.max = max
        self.units = units
        self.barwidth = barwidth
        if bulbwidth is None:
            bulbwidth = 2 * barwidth
        self.bulbwidth = bulbwidth
        self.linewidth = linewidth
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.padding_x = padding_x
        self.padding_y = padding_y

        self.ax = None

        self._temp_bulb = None
        self._temp_bar = None
        self._temp_text = None

    @property
    def bar_height(self):
        return self.max - self.origin_y

    @property
    def origin_y(self):
        """y-coordinate for the bottom of the bar and the middle of the bulb."""
        return self.min + self.bulbwidth / 2

    @property
    def xmax(self):
        return self.barwidth + self.padding_x

    @property
    def xmin(self):
        return -self.barwidth - self.padding_x

    @property
    def ymax(self):
        return self.max + self.padding_y

    @property
    def ymin(self):
        return self.min - self.padding_y

    def draw(
        self, temperature, ax=None, display_value=True, title=None, description=None
    ):
        """Draw a thermometer with a temperature reading.

        Parameters
        ----------
        temperature : float
            Temperature to show.
        ax : None or matplotlib.axes.Axes, optional
            Axes object to draw to. If not given, the method will create a new Axes
            object in a new figure.
        display_value : bool, optional
            If True (default), display the current value to the left.
        title : None or str, optional
            String to use as figure title.
        description : None or str, optional
            Description to display at the bottom.

        """
        # Draw outline if necessary
        if self.ax is None:
            self.draw_outline(ax=ax)

        if ax is None:
            ax = self.ax

        self._create_bar(ax, temperature)
        if title:
            ax.get_figure().suptitle(title)

        if description:
            ax.set_xlabel(localize(description))

        if self._temp_text is not None:
            self._temp_text.remove()

        if display_value:
            self._temp_text = ax.text(
                self.xmax,
                temperature,
                f"{temperature:.1f}{self.units}",
                horizontalalignment="left",
                verticalalignment="center",
                color=self.facecolor,
            )

    def draw_outline(self, ax=None):
        """Draw outline of the thermometer.

        Parameters
        ----------
        ax : None or matplotlib.axes.Axes, optional
            Axes object to draw to. If not given, the method will create a new Axes
            object in a new figure.

        Returns
        -------
        matplotlib.axes.Axes:
            Axes object containing the thermometer.

        """
        if ax is None:
            _, ax = plt.subplots()

        # NOTE: Don't know how to draw the common outline of two patches, so here we
        # cheat by first drawing an "outer" part and then an "inner" part filled with
        # white

        outer_bulb = patches.Circle(
            (0, self.origin_y),
            radius=self.bulbwidth / 2,
            color=self.edgecolor,
            linewidth=0,
        )
        outer_bar = patches.Rectangle(
            (-self.barwidth / 2, self.origin_y),
            width=self.barwidth,
            height=self.bar_height,
            color=self.edgecolor,
            linewidth=0,
        )
        inner_bulb = self._get_inner_bulb(color="w")
        inner_bar = self._get_inner_bar(color="w")

        ax.add_patch(outer_bulb)
        ax.add_patch(outer_bar)
        ax.add_patch(inner_bulb)
        ax.add_patch(inner_bar)

        ax.set_aspect("equal")
        ax.set_xlim(self.xmin, self.xmax)
        ax.set_ylim(self.ymin, self.ymax)
        ax.set_xticks([])
        ax.spines[["right", "top", "bottom"]].set_visible(False)

        yticks = [tick for tick in ax.get_yticks() if self.min <= tick <= self.max]
        yticklabels = [f"{tick:.0f}{self.units}" for tick in yticks]
        ax.set_yticks(yticks, yticklabels)

        self.ax = ax

        return ax

    def _create_bar(self, ax, temperature):
        # Remove old elements
        if self._temp_bar is not None:
            self._temp_bar.remove()
        if self._temp_bulb is not None:
            self._temp_bulb.remove()

        width = self.xmax - self.xmin
        height = temperature - self.min

        # Need two temperature patches, one for the bulb part and one for the bar
        self._temp_bulb = patches.Rectangle(
            (self.xmin, self.min), width=width, height=height, color=self.facecolor
        )
        self._temp_bar = patches.Rectangle(
            (self.xmin, self.min), width=width, height=height, color=self.facecolor
        )

        ax.add_patch(self._temp_bulb)
        ax.add_patch(self._temp_bar)

        inner_bulb = self._get_inner_bulb()
        inner_bar = self._get_inner_bar()

        # Need to add these clip patches to ax to get the coordinates right
        ax.add_patch(inner_bulb)
        ax.add_patch(inner_bar)

        self._temp_bulb.set_clip_path(inner_bulb)
        self._temp_bar.set_clip_path(inner_bar)

    def _get_inner_bulb(self, color="none"):
        inner_bulb = patches.Circle(
            (0, self.origin_y),
            radius=self.bulbwidth / 2 - self.linewidth,
            color=color,
            linewidth=0,
        )
        return inner_bulb

    def _get_inner_bar(self, color="none"):
        inner_bar = patches.Rectangle(
            (-self.barwidth / 2 + self.linewidth, self.origin_y),
            width=self.barwidth - 2 * self.linewidth,
            height=self.bar_height - self.linewidth,
            color=color,
            linewidth=0,
        )
        return inner_bar
