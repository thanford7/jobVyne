import lxml.html as lh
import requests


class ProxyListGetterBase:
    
    def __init__(self, anonym=False, elite=False, google=False, https=True):
        self.anonym = anonym
        self.elite = elite
        self.google = google
        self.schema = 'https' if https else 'http'


class ProxyListGetter1(ProxyListGetterBase):

    PROXY_WEBSITES = [
        'https://free-proxy-list.net',
        'https://www.us-proxy.org',
        'https://free-proxy-list.net/uk-proxy.html',
        'https://www.sslproxies.org'
    ]

    ALLOWED_COUNTRY_CODES = ['US', 'CA', 'GB']
    
    def get_proxy_list(self):
        proxies = []
        for website in self.PROXY_WEBSITES:
            page = requests.get(website)
            doc = lh.fromstring(page.content)
            tr_elements = doc.xpath('//*[@id="list"]//tr')
            proxies += [f'{tr_elements[i][0].text_content()}:{tr_elements[i][1].text_content()}'
                for i in range(1, len(tr_elements)) if self.is_meets_criteria(tr_elements[i])]
        return proxies

    def is_meets_criteria(self, row_elements):
        country_criteria = True if not self.ALLOWED_COUNTRY_CODES else row_elements[2].text_content() in self.ALLOWED_COUNTRY_CODES
        elite_criteria = True if not self.elite else 'elite' in row_elements[4].text_content()
        anonym_criteria = True if (not self.anonym) or self.elite else 'anonymous' == row_elements[4].text_content()
        switch = {'yes': True, 'no': False}
        google_criteria = True if self.google is None else self.google == switch.get(row_elements[5].text_content())
        https_criteria = True if self.schema == 'http' else row_elements[6].text_content().lower() == 'yes'
        return all([country_criteria, elite_criteria, anonym_criteria, google_criteria, https_criteria])
    
    
class ProxyListGetter2(ProxyListGetterBase):
    ALLOWED_COUNTRY_CODES = ['United States', 'Canada']
    
    def get_proxy_list(self):
        # TODO: This site needs to be loaded with JS. The proxytable is dynamic
        page = requests.get('https://proxyscrape.com/free-proxy-list')
        doc = lh.fromstring(page.content)
        tr_elements = doc.xpath('//*[@id="proxytable"]//tr')
        proxy_list = [f'{tr_elements[i][0].text_content()}:{tr_elements[i][1].text_content()}'
                    for i in range(1, len(tr_elements)) if self.is_meets_criteria(tr_elements[i])]
        return proxy_list
    
    def is_meets_criteria(self, row_elements):
        return True if not self.ALLOWED_COUNTRY_CODES else row_elements[3].text_content() in self.ALLOWED_COUNTRY_CODES


class ProxyGetter:

    def __init__(self, timeout=0.5, anonym=False, elite=False, google=False, https=True):
        self.timeout = timeout
        self.anonym = anonym
        self.elite = elite
        self.google = google
        self.schema = 'https' if https else 'http'
        self.proxy_list = ProxyListGetter1(anonym=False, elite=False, google=False, https=True).get_proxy_list()
        self.proxy_list += ProxyListGetter2(anonym=False, elite=False, google=False, https=True).get_proxy_list()
        
    def get_proxies(self, proxy_count=1, is_raise_error=False):
        working_proxies = []
        while proxy_count > len(working_proxies) and self.proxy_list:
            proxy = f'http://{self.proxy_list.pop()}'
            try:
                if self.is_proxy_working(proxy):
                    working_proxies.append(proxy)
            except requests.exceptions.RequestException:
                continue
        
        if is_raise_error and len(working_proxies) < proxy_count:
            raise Exception(f'Could not find the requested number of proxies ({proxy_count}). Found {len(working_proxies)}')
        
        if not working_proxies:
            raise Exception('Could not find any working proxies')
        
        return working_proxies

    def is_proxy_working(self, proxy):
        url = f'{self.schema}://www.google.com'
        ip = proxy.split(':')[1][2:]
        with requests.get(url, proxies={self.schema: proxy}, timeout=self.timeout, stream=True) as r:
            if r.raw.connection.sock and r.raw.connection.sock.getpeername()[0] == ip:
                return True
        return False
