'''
curl -X POST localhost:3001 \
    -H 'Content-Type: application/json' \
    -d @./testProject.json
'''

import requests

client = requests.session()
URL = "http://localhost:5002/"

query = {
    "Query":"Select UserName,ProjectName FROM Projects WHERE UserName='manav' AND ProjectName='Tausendpfund';",
    "Fetch":True
}

response = client.post(URL, data=query)
print (response)
print (response.json())