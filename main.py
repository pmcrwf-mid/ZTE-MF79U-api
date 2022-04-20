import requests
from loguru import logger
import json
import time
import base64

basic_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/99.0.4844.84 "
                               "Safari/537.36 "
                               "OPR/85.0.4341.60 (Edition Yx 05)",
                 "X-Requested-With": "XMLHttpRequest",
                 "Accept": "application/json, text/javascript, */*; q=0.01",
                 "Accept-Encoding": "gzip, deflate",
                 "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                 "dnt": "1",
                 "sec-gpc": "1"
                 }


def load_settings():
    with open("settings.json", "r") as settings_file:
        return json.load(settings_file)


def base64_encode(string: str) -> str:
    return str(base64.b64encode(bytes(string, 'utf-8')), encoding='utf-8')


def auth(password):
    answer = requests.post("http://192.168.0.1/goform/goform_set_cmd_process",
                           data={'isTest': 'false',
                                 'goformId': 'LOGIN',
                                 'password': base64_encode(password)},
                           headers=basic_headers | {
                               "Origin": "http://192.168.0.1",
                               "Referer": "http://192.168.0.1/index.html"})
    if answer.json()['result'] != "0":
        raise Exception("Auth Error")
    logger.debug(f"Auth: {answer}")
    return {"stok": answer.cookies.get("stok")}


def get_data_1(cookie):
    answer = requests.get("http://192.168.0.1/goform/goform_get_cmd_process?"
                          "isTest=false&"
                          "cmd=m_ssid_enable%2CRadioOff%2CNoForwarding%2Cm_NoForwarding%2CWPAPSK1%2Cm_WPAPSK1%2C"
                          "wifi_attr_max_station_number%2CSSID1%2CAuthMode%2CHideSSID%2CMAX_Access_num%2C"
                          "EncrypType%2Cm_SSID%2Cm_AuthMode%2Cm_HideSSID%2Cm_MAX_Access_num%2Cm_EncrypType%2C"
                          "qrcode_display_switch%2Cm_qrcode_display_switch&multi_data=1",
                          headers=basic_headers | {"Referer": "http://192.168.0.1/index.html"},
                          cookies=cookie)
    logger.debug(f"Get data #1: {answer}")
    return answer


def get_data_2(cookie):
    answer = requests.get("http://192.168.0.1/goform/goform_get_cmd_process?"
                          "isTest=false&cmd=apn_interface_version%2Cwifi_coverage%2Cm_ssid_enable%2Cimei%2C"
                          "modem_msn%2CBSSID%2Csim_iccid%2Cnetwork_type%2Cnetwork_provider%2C"
                          "network_provider_fullname%2Cprefer_dns_auto%2Cstandby_dns_auto%2Crssi%2C"
                          "rscp%2Clte_rsrp%2Clte_rssi%2Clte_snr%2Cecio%2Cnet_select%2Cwan_active_band%2C"
                          "mdm_mcc%2Cmdm_mnc%2Ccell_id%2Clac_code%2Clte_pci%2Clte_rsrq%2Cimsi%2Csim_imsi%2C"
                          "rplmn_num%2Ccr_version%2Cwa_version%2Chardware_version%2Cweb_version%2Cwa_inner_version%2C"
                          "MAX_Access_num%2CSSID1%2CAuthMode%2CWPAPSK1_encode%2Cm_SSID%2Cm_AuthMode%2Cm_HideSSID%2C"
                          "m_WPAPSK1_encode%2Cm_MAX_Access_num%2Clan_ipaddr%2Clan_netmask%2Cmac_address%2Cmsisdn%2C"
                          "LocalDomain%2Cm_profile_name%2Cenodeb_id%2Cwan_ipaddr%2Cstatic_wan_ipaddr%2C"
                          "ipv6_wan_ipaddr%2Cipv6_pdp_type%2Cipv6_pdp_type_ui%2Cpdp_type%2Cpdp_type_ui%2C"
                          "opms_wan_mode%2Cppp_status%2Ccable_wan_ipaddr%2Croam_setting_option%2Crouter_mode_gateway%2C"
                          "dhcpStart%2CdhcpEnd&multi_data=1",
                          headers=basic_headers | {"Referer": "http://192.168.0.1/index.html"},
                          cookies=cookie)
    logger.debug(f"Get data #2: {answer}")
    return answer
    

if __name__ == '__main__':
    settings = load_settings()
    logger.debug("Settings loaded")
    cookies = auth(settings["password"])
    logger.debug(f"Cookies: {cookies}")
    info_dict = {}
    info_dict.update(get_data_1(cookies).json())
    info_dict.update(get_data_2(cookies).json())
    logger.debug(info_dict)
    logger.info(f"SSID1: {info_dict['SSID1']}")
