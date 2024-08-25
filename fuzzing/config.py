# config.py

import webcolors
import random

# Additional fonts for replacement including styles
alternative_fonts = [
    "Arial", "Arial Bold", "Arial Italic", "Verdana", "Verdana Bold", "Verdana Italic",
    "Tahoma", "Tahoma Bold", "Tahoma Italic", "Trebuchet MS", "Trebuchet MS Bold", "Trebuchet MS Italic",
    "Times New Roman", "Times New Roman Bold", "Times New Roman Italic",
    "Georgia", "Georgia Bold", "Georgia Italic", "Bold", "Italic",
    "Garamond", "Garamond Bold", "Garamond Italic",
    "Courier New", "Courier New Bold", "Courier New Italic",
    "Brush Script MT", "Impact", "Comic Sans MS", "Lucida Sans","opendyslexic",
    "Palatino", "Century Gothic", "Gill Sans", "Calibri", "Cambria", "Candara", "Constantia", "Corbel"
]

# String boolean replacements
all_string_bools = {
    "no": "yes", "NO": "YES", 'No': 'Yes', "yes": "no", "YES": "NO",
    "on": "off", "ON": "OFF", "true": "false", "TRUE": "FALSE",
    "enable": "disable", "ENABLE": "DISABLE", "activate": "deactivate",
    "ACTIVATE": "DEACTIVATE", "active": "deactive", "ACTIVE": "DEACTIVE",
    "isOn": "isOff", "ISON": "ISOFF", "IsOn": "IsOff", "isON": "isOFF",
    "On": "Off", "off": "on", "OFF": "ON", "false": "true", "FALSE": "TRUE",
    "disable": "enable", "DISABLE": "ENABLE", "deactivate": "activate",
    "DEACTIVATE": "ACTIVATE", "deactive": "active", "DEACTIVE": "ACTIVE",
    "isOff": "isOn", "ISOFF": "ISON", "IsOff": "IsOn", "isOFF": "isON",
    "Off": "On", "open": "close", "OPEN": "CLOSE", "close": "open",
    "CLOSE": "OPEN", "offline": "online", 'ENABLED': 'DISABLED',
    'DISABLED': 'ENABLED'
}

# Locales and country codes
locales = [
    "af", "af-NA", "af-ZA", "agq", "agq-CM", "ak", "ak-GH", "am", "am-ET", "ar", "ar-001", "ar-AE", "ar-BH",
    "ar-DJ", "ar-DZ", "ar-EG", "ar-EH", "ar-ER", "ar-IL", "ar-IQ", "ar-JO", "ar-KM", "ar-KW", "ar-LB", "ar-LY",
    "ar-MA", "ar-MR", "ar-OM", "ar-PS", "ar-QA", "ar-SA", "ar-SD", "ar-SO", "ar-SS", "ar-SY", "ar-TD", "ar-TN",
    "ar-YE", "as", "as-IN", "asa", "asa-TZ", "az", "az-Cyrl", "az-Cyrl-AZ", "az-Latn", "az-Latn-AZ", "bas", "bas-CM",
    "be", "be-BY", "bem", "bem-ZM", "bez", "bez-TZ", "bg", "bg-BG", "bm", "bm-ML", "bn", "bn-BD", "bn-IN", "bo",
    "bo-CN", "bo-IN", "br", "br-FR", "brx", "brx-IN", "bs", "bs-Cyrl", "bs-Cyrl-BA", "bs-Latn", "bs-Latn-BA", "ca",
    "ca-AD", "ca-ES", "ca-ES-VALENCIA", "ca-FR", "ca-IT", "ce", "ce-RU", "cgg", "cgg-UG", "chr", "chr-US", "ckb",
    "ckb-IQ", "ckb-IR", "cs", "cs-CZ", "cu", "cu-RU", "cy", "cy-GB", "da", "da-DK", "da-GL", "dav", "dav-KE", "de",
    "de-AT", "de-BE", "de-CH", "de-DE", "de-IT", "de-LI", "de-LU", "dje", "dje-NE", "dsb", "dsb-DE", "dua", "dua-CM",
    "dyo", "dyo-SN", "dz", "dz-BT", "ebu", "ebu-KE", "ee", "ee-GH", "ee-TG", "el", "el-CY", "el-GR", "en", "en-001",
    "en-150", "en-AE", "en-AG", "en-AI", "en-AS", "en-AT", "en-AU", "en-BB", "en-BE", "en-BM", "en-BS", "en-BW",
    "en-BZ", "en-CA", "en-CC", "en-CH", "en-CK", "en-CM", "en-CX", "en-CY", "en-DE", "en-DG", "en-DK", "en-DM",
    "en-ER", "en-FI", "en-FJ", "en-FK", "en-FM", "en-GB", "en-GD", "en-GG", "en-GH", "en-GI", "en-GM", "en-GU",
    "en-GY", "en-HK", "en-IE", "en-IL", "en-IM", "en-IN", "en-IO", "en-JE", "en-JM"]

def get_random_font():
    return random.sample(alternative_fonts, 20)

def get_random_string_bool():
    return all_string_bools[random.choice(list(all_string_bools.keys())).lower()]

def get_random_locale():
    return random.choice(locales)

