import requests
import json
import sys
import argparse

class Grafana():

    def fetch(self,url="",target="",warning=0,threshold=0):
        rsp = requests.get(url)
        rsp_json = rsp.json()
        num_targets = len(rsp_json)
        counter = 0
        if num_targets < 1:
            print("UNKNOWN")
            sys.exit(3)

        for i in range(num_targets):
            if rsp_json[i]['target'] == target:
                datapoints = len(rsp_json[i]['datapoints'])
                for j in range(datapoints):
                    counter = 1
                    if rsp_json[i]['datapoints'][j][0] != None and rsp_json[i]['datapoints'][j][0] > warning:
                        print("CRITICAL")
                        sys.exit(2)
                    if rsp_json[i]['datapoints'][j][0] != None and rsp_json[i]['datapoints'][j][0] > threshold:
                        print("WARNING")
                        sys.exit(1)

        if counter == 0:
            print("UNKNOWN")
            sys.exit(3)
        
        print("OK")
        
def url_merger(host,port,metric):
    if port == 80 or port == 443 :
        return host + metric
    
    return host + ":" + port + metric


def parse_args():
    parser = argparse.ArgumentParser(description='Graphite Check Script',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--hostgraphite', default='https://play.grafana.org')                    
    parser.add_argument('--portgraphite', default='443')                
    parser.add_argument('--metric', default='/api/datasources/proxy/1/render?target=aliasByNode(movingAverage(scaleToSeconds(apps.fakesite.*.counters.requests.count,%201),%202),%202)&format=json&from=-5min')                
    parser.add_argument('-target', default='')                     
    parser.add_argument('-warning', default=0)              
    parser.add_argument('-threshold', default=0)

    return parser.parse_args()

def main():
    p = parse_args()
    url = url_merger(p.hostgraphite,p.portgraphite,p.metric)
    gfn = Grafana()
    gfn.fetch(url=url,target=p.target, warning= p.warning, threshold=p.threshold)

if __name__ == "__main__":
    main()



