import pandas as pd
import re
from bisect import bisect
import netaddr

ip_df = pd.read_csv("ip2location.csv")

def lookup_region(ip):
    other_ip = re.sub(r"[A-Za-z]", "0", ip)
    int_ip = int(netaddr.IPAddress(other_ip))
    ip_idx = (bisect(ip_df["low"], int_ip))-1
    
    return ip_df["region"][ip_idx]

class Filing:
    def __init__(self, html):
        self.dates = []
        for val in re.findall(r"((19|20)\d\d-(0?[1-9]|1[012])-([12][0-9]|3[01]|0?[1-9]))", html):
            self.dates.append(val[0])
        if re.findall(r"SIC=(\d+)", html) == []:
            self.sic = None
        else:
            self.sic = int((re.findall(r"SIC=(\d+)", html)[0]))
        self.addresses = []
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []
            list_0 = re.findall(r"<span class=\"mailerAddress\">([\s\S]+?)</span>", addr_html)
            if list_0 != []:
                for line in re.findall(r"<span class=\"mailerAddress\">([\s\S]+?)</span>", addr_html):
                    lines.append(line.strip())
                self.addresses.append("\n".join(lines))
        
    def state(self):
        state = []
        for address in self.addresses:
            state.extend(re.findall(r"(?<!\w)([A-Z]{2})\s\d{5}", address))
            if len(state) != 0:
                return state[0]
        return None