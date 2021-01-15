import json
import web_scraping.text_parser as parser
if __name__ == "__main__":
    json_output = parser.read_web_text_json_file('output/searches/train/site_info.json')
    with open('test.json', 'w') as outfile:
        json.dump(json_output, outfile, indent=4)
    
