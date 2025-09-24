
import time
import os

from ipsectest import setup_driver,ipsec
from shadowsockstest import setup_driver,shadowsocks
from VMesstest import setup_driver,VMess
from wireguardtest import setup_driver,wireguard
import servernamecapture
import protocolnamecapture
import os


def main():

    driver_server = servernamecapture.setup_driver()
    server_names = servernamecapture.Servers_name(driver_server)  # Make sure it returns a list
    time.sleep(2)

    # driver_server=protocolnamecapture.setup_driver()
    # #protocols_name=protocolnamecapture.protocols_name_collection(driver_server)


    # for var in ["HTTP_PROXY", "HTTPS_PROXY", "SOCKS_PROXY", "ALL_PROXY"]:
    #     os.environ.pop(var, None)

    #
    # driver = setup_driver()
    # print("IN the driver")
    # VMess(driver)
    # time.sleep(10)

    # driver = setup_driver()
    # ipsec(driver)
    # time.sleep(10)
    #






if __name__ == "__main__":
    main()
