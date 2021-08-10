from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from fake_headers import Headers
import requests

class Random_Proxy:
    def __init__(self):
        self.proxy=self.proxy_create()
        self.crawling()
    def proxy_create(self):
        self.req_proxy=RequestProxy()
        proxy=self.test_proxy()
        return proxy
    def test_proxy(self):
        test_url='https://www.google.com/search?q={}&as_qdr=d&as_sitesearch={}'.format('고양이','dcinside.com')
        while True: # 제대로된 프록시가 나올때까지 무한반복 
            requests = self.req_proxy.generate_proxied_request(test_url)
            if requests is not None and requests.status_code==200:
                print("\t Response: ip={0}".format(u''.join(requests.text).encode('utf-8')))
                proxy = self.req_proxy.current_proxy
                break
            else:
                continue
        return proxy # 잘작동된 proxy를 뽑아준다. 
    def crawling(self):
        header=Headers(
            browser='chrome',
            os="win",
            headers=True
        )
        self.headers=header.generate()

        self.proxies={}
        self.proxies['http']='http://%s' % self.proxy

        url='https://www.google.com/search?q={}&as_qdr=d&as_sitesearch={}'.format('고양이','dcinside.com')

        res=requests.get(url,headers=self.headers).content

        print(res)

if __name__=="__main__":
    Random_Proxy()