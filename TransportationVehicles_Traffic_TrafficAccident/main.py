import sys
sys.path.append('../')
import parse_rule_file
import json

if __name__=='__main__':
    rule_parser = parse_rule_file.rule_parser('./concept.txt','./rule.txt')
    for lines in open('/mnt/nlp/corpora/text-classify-traindata-google/cur/data_flush/data_to_flush_202006.res.final'):
        data = lines.strip().split('\t')
        label = data[0]
        jd = json.loads(data[1])
        url = jd['url']
        title = jd['title']
        content = jd['content']
        if 'TransportationVehicles' in label:
            url_res = rule_parser.match(url.lower())
            title_res = rule_parser.match(title.lower())
            content_res = rule_parser.match(content.lower())
            if title_res['r_1']:
                print('TransportationVehicles_Traffic_TrafficAccident\t'+url+'\t'+title)
        
