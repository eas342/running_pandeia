import json
import yaml

dat = json.load(open('json/readme_example.json'))

yaml.safe_dump(dat,open('yaml/readme_example.yaml','w'),default_flow_style=False)

