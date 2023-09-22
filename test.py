# import json
#
# import requests
#
# url = "https://scrape.smartproxy.com/v1/tasks"
#
# payload = {
#       "target": "universal",
#       "url": "https://www.facebook.com/marketplace/112356482109204/propertyrentals",
#       "locale": "en",
#       "geo": "United States",
#       "device_type": "desktop",
#       "headless": "html"
# }
#
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "authorization": "Basic VTAwMDAxMjEyNzU6bEI5d3h6Q25XVzZ0N2lwZTdh"
# }
#
# response = requests.post(url, json=payload, headers=headers)
# re = json.loads(response.text)['results'][0]['content']
# print(re)
# print(response.text)
from src.database.models import Product, UserSite
u = UserSite(password='sesgsdf', email='sdf@mail.com')
d = dict(u.__dict__)
print(d.pop('_sa_instance_state'))
# print([i.name for i in [*Product.metadata.tables.get('product').columns]])