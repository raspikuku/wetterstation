import smbus


class BH1750 :
    def __init__(self, bus = 1, address = 0x23):
        self.bus = smbus.SMBus(bus)
        self.address = address

    def convertToNumber(self, data):
        return (data[1] + (256 * data[0])) / 1.2

    def read(self, mode = 0x20):
        data = self.bus.read_i2c_block_data(self.address, mode)
        return self.convertToNumber(data)

