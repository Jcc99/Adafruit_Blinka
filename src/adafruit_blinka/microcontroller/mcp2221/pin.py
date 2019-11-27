from .mcp2221 import mcp2221

class Pin:
    """A basic Pin class for use with MCP2221."""

    # pin modes
    OUT     = 0
    IN      = 1
    ADC     = 2
    DAC     = 3
    # pin values
    LOW     = 0
    HIGH    = 1

    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None

    def init(self, mode=IN, pull=None):
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        if mode in (Pin.IN, Pin.OUT):
            mcp2221.gp_set_mode(self.id, mcp2221.GP_GPIO)
            mcp2221.gpio_set_direction(self.id, mode)
        elif mode == Pin.ADC:
            mcp2221.gp_set_mode(self.id, mcp2221.GP_ALT0)
            mcp2221.adc_configure()
        elif mode == Pin.DAC:
            mcp2221.gp_set_mode(self.id, mcp2221.GP_ALT1)
            mcp2221.dac_configure()
        else:
            raise ValueError("Incorrect pin mode: {}".format(mode))
        self._mode = mode

    def value(self, val=None):
        # Digital In / Out
        if self._mode in (Pin.IN, Pin.OUT):
            # digital read
            if val is None:
                return mcp2221.gpio_get_pin(self.id)
            # digital write
            elif val in (Pin.LOW, Pin.HIGH):
                mcp2221.gpio_set_pin(self.id, val)
            # nope
            else:
                raise ValueError("Invalid value for pin.")
        # Analog In
        elif self._mode == Pin.ADC:
            if val is None:
                # MCP2221 ADC is 10 bit, scale to 16 bit per CP API
                return mcp2221.adc_read(self.id) * 64
            else:
                # read only
                raise AttributeError("'AnalogIn' object has no attribute 'value'")
        # Analog Out
        elif self._mode == Pin.DAC:
            if val is None:
                # write only
                raise AttributeError("unreadable attribute")
            else:
                # scale 16 bit value to MCP2221 5 bit DAC (yes 5 bit)
                mcp2221.dac_write(self.id, val // 2048)
        else:
            raise RuntimeError("No action for mode {} with value {}".format(self._mode, val))


# create pin instances for each pin
G0 = Pin(0)
G1 = Pin(1)
G2 = Pin(2)
G3 = Pin(3)

SCL = Pin()
SDA = Pin()