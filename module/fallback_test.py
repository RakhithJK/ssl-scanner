import socket
from util import *

fallback_to_ssl3 = '160300009c010000980300b8cd74dbfed2e4c86f90d130f07421f8d33da498d35ca56370f88d51373c26b4000070c014c00a00390038003700360088008700860085c00fc005003500840095c013c0090033003200310030009a0099009800970045004400430042c00ec004002f0096004100070094c011c0070066c00cc002000500040092c012c008001600130010000dc00dc003000a009300ff5600020100'
fallback_to_tls10 = '16030100ed010000e90301e54f7ee978946c157a3ae837352a4c4ef81731a11c9a5d173d8f82cc60f7d532000070c014c00a00390038003700360088008700860085c00fc005003500840095c013c0090033003200310030009a0099009800970045004400430042c00ec004002f0096004100070094c011c0070066c00cc002000500040092c012c008001600130010000dc00dc003000a009300ff5600020100004f000b000403000102000a003a0038000e000d0019001c000b000c001b00180009000a001a00160017000800060007001400150004000500120013000100020003000f0010001100230000000f000101'
fallback_to_tls11 = '16030100ed010000e9030245fd7dc91832226552f54116b1b755bed8f854ee957a0ca0db21b2c05052c98c000070c014c00a00390038003700360088008700860085c00fc005003500840095c013c0090033003200310030009a0099009800970045004400430042c00ec004002f0096004100070094c011c0070066c00cc002000500040092c012c008001600130010000dc00dc003000a009300ff5600020100004f000b000403000102000a003a0038000e000d0019001c000b000c001b00180009000a001a00160017000800060007001400150004000500120013000100020003000f0010001100230000000f000101'

def tryConnect(host, port, version) :
    if version == 0 : hello = addNecessaryExtensionToHello(fallback_to_ssl3, host)
    elif version == 1 : hello = addNecessaryExtensionToHello(fallback_to_tls10, host)
    elif version == 2 : hello = addNecessaryExtensionToHello(fallback_to_tls11, host)

    return tryHandshake(host, port, hello) == version

class FallbackTest(Test) :
    def start(self) :
        protocol = list(filter(lambda x : self._result.getResult(x[0]), [('offer_tls12',3), ('offer_tls11',2), ('offer_tls10',1), ('offer_ssl3',0)]))

        if len(protocol) <= 1 :
            print("[FALLBACK] Unable to test: Available protocol count is <= 1")
            self._result.addResult('fallback_support',False)
            return

        # Try connect to prot[1] (lower)
        self._result.addResult('fallback_support',not tryConnect(self._host, self._port, protocol[1][1]))

        if not self._result.getResult('fallback_support') :
            self._result.addVulnerability('fallback_support')