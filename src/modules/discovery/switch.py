class Switch(object):

    manufacturer = ""
    ip = ""
    serial = ""
    list_vlan = []
    login = {}
    version_software = ""
    version_firmware = ""
    uptime = ""

    def __init__(self, manufacturer, ip):
        self.manufacturer = manufacturer
        self.ip = ip

    def get_manufacturer(self):
        return self.manufacturer

    def get_ip(self):
        return self.ip

    def get_serial(self):
        return self.serial

    def get_vlans(self):
        return self.list_vlan

    def set_login(self, user, password):
        self.login[user] = password

    def get_login(self):
        return self.login

    def set_version_software(self, software):
        self.version_software = software

    def get_version_software(self):
        return self.version_software

    def set_version_firmware(self, firmware):
        self.version_firmware = firmware

    def get_version_firmware(self):
        return self.version_firmware

    def set_uptime(self, uptime):
        self.uptime = uptime

    def get_uptime(self):
        return self.uptime
