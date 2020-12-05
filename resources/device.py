import sys

class Device(object):
    def __init__(self, device_identifier, version):
        super().__init__()

        self.device = device_identifier
        self.cellular = self.has_baseband()
        self.maggie = self.has_maggie()
        self.homer = self.has_homer()
        self.multitouch = self.has_multitouch()
        self.version = version
        self.template = self.get_wiki_template()

    def has_baseband(self):
        if self.device.startswith('iPhone'):
            return True

        elif self.device.startswith('iPod'):
            return False

        elif self.device.startswith('iPad'):
            cellular_ipads = ['iPad4,2', 'iPad4,3', 'iPad5,4', 'iPad11,4', 'iPad13,2', 'iPad6,8', 'iPad6,4', 'iPad7,2', 'iPad7,4', 'iPad8,3', 'iPad8,4', 'iPad8,7', 'iPad8,8', 'iPad8,10', 'iPad8,12', 'iPad4,5', 'iPad4,6', 'iPad4,8', 'iPad4,9', 'iPad5,2', 'iPad11,2']
            if self.device in cellular_ipads:
                return True
            else:
                return False
    
    def has_maggie(self):
        maggie_devices = ['iPhone9,1', 'iPhone9,2', 'iPhone9,3', 'iPhone9,4', 'iPhone10,1', 'iPhone10,2', 'iPhone10,3', 'iPhone10,4', 'iPhone10,5', 'iPhone10,6']
        if self.device in maggie_devices:
            return True
        else:
            return False

    def has_multitouch(self):
        multitouch_devices = ['iPad7,11', 'iPad7,12'] # No need to include A11 devices, as all A11 devices have Multitouch.
        if self.device in multitouch_devices:
            return True
        else:
            return False

    def has_homer(self):
        homer_devices = ['iPhone9,1', 'iPhone9,2', 'iPhone9,3', 'iPhone9,4']
        if self.device in homer_devices:
            return True
        else:
            return False

    def get_wiki_template(self):
        pre_a4_devices = ['iPod3,1', 'iPhone2,1', 'iPod2,1', 'iPod1,1', 'iPhone1,1', 'iPhone1,2']
        a4_devices = ['AppleTV2,1', 'iPad1,1', 'iPhone3,1', 'iPhone3,2', 'iPhone3,3', 'iPod4,1']
        a5_devices = ['iPad2,1', 'iPad2,2', 'iPad2,3', 'iPad2,4', 'iPhone4,1', 'AppleTV3,1', 'iPod5,1', 'iPad2,5', 'iPad2,6', 'iPad2,7', 'iPad3,1', 'iPad3,2', 'iPad3,3', 'AppleTV3,2']
        a6_devices = ['iPhone5,1', 'iPhone5,2', 'iPhone5,3', 'iPhone5,4', 'iPad3,4', 'iPad3,5', 'iPad3,6']
        a7_devices = ['iPad4,1', 'iPad4,2', 'iPad4,3', 'iPad4,4', 'iPad4,5', 'iPad4,6', 'iPad4,7', 'iPad4,8', 'iPad4,9', 'iPhone6,1', 'iPhone6,2']
        a8_devices = ['iPad5,1', 'iPad5,2', 'iPad5,3', 'iPad5,4', 'iPhone7,1', 'iPhone7,2', 'iPod7,1']
        a9_devices = ['iPad6,11', 'iPad6,12', 'iPad6,3', 'iPad6,4', 'iPad6,7', 'iPad6,8', 'iPhone8,1', 'iPhone8,2', 'iPhone8,4']
        a10_devices = ['iPad7,1', 'iPad7,2', 'iPad7,11', 'iPad7,12', 'iPad7,5', 'iPad7,6', 'iPhone9,1', 'iPhone9,2', 'iPhone9,3', 'iPhone9,4', 'iPod9,1', 'iPad7,1', 'iPad7,2', 'iPad7,3', 'iPad7,4']
        a11_devices = ['iPhone10,1', 'iPhone10,2', 'iPhone10,4', 'iPhone10,5', 'iPhone10,3', 'iPhone10,6']

        self.required_components = {}

        if self.device in pre_a4_devices or self.device in a4_devices or self.device in a5_devices or self.device in a6_devices:
            if self.cellular:
                wiki_template = 'resources/templates/32bit_cellular.txt'
            else:
                wiki_template = 'resources/templates/32bit_nocellular.txt'

            if self.version[:2] == '10':
                wiki_template = f'{wiki_template[:-4]}_ios10.txt'

        if self.device in a7_devices or self.device in a8_devices:
            if self.cellular:
                wiki_template = 'resources/templates/a7a8_cellular.txt'
            else:
                wiki_template = 'resources/templates/a7a8_nocellular.txt'

        elif self.device in a9_devices:
            sys.exit('[ERROR] A9 devices are not currently supported. Exiting...')

        elif self.device in a10_devices:
            if self.cellular:
                wiki_template = 'resources/templates/a10_cellular.txt'
            else:
                wiki_template = 'resources/templates/a10_nocellular.txt'
            
            if self.homer:
                wiki_template = f'{wiki_template[:-4]}_maggie_homer.txt' # All devices with Homer also have Maggie

            if self.multitouch:
                wiki_template = f'{wiki_template[:-4]}_multitouch.txt'
            
        elif self.device in a11_devices:
            wiki_template = 'resources/templates/a11_cellular_maggie.txt'

            if int(self.version[:2]) >= 13:
                wiki_template = f'{wiki_template[:-4]}_adc.txt'

        if '_cellular' in wiki_template:
            self.required_components["baseband"] = True
        else:
            self.required_components["baseband"] = False

        if '_maggie' in wiki_template:
            self.required_components["maggie"] = True
            self.required_components["liquiddetect"] = True
        else:
            self.required_components["maggie"] = False
            self.required_components["liquiddetect"] = False

        if '_homer' in wiki_template:
            self.required_components["homer"] = True
        else:
            self.required_components["homer"] = False

        if '_adc' in wiki_template:
            self.required_components["isp"] = True
        else:
            self.required_components["isp"] = False

        if self.device in a9_devices or self.device in a10_devices or self.device in a11_devices:
            self.required_components["aop"] = True
        else:
            self.required_components["aop"] = False

        if self.device in a11_devices:
            self.required_components["audiocodec"] = True
            self.required_components["multitouch"] = True
        else:
            self.required_components["audiocodec"] = False
            self.required_components["multitouch"] = False

        if self.multitouch:
            self.required_components["multitouch"] = True

        return wiki_template