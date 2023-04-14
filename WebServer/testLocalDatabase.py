
import requests
import unittest
import time

client = requests.session()

URL = "https://p-energyanalysis.de/database/"
Id = "f76ba64860271dd9dd21867e387004d1"
URL = "http://localhost:8080/database/"

response = client.get(URL, headers={'Id': Id})
csrfToken = response.json()['csrf_token']

class databaseTest(unittest.TestCase):
    def testQueryTestProject(self):
        query = {
            "Query":"Select UserName,ProjectName FROM Projects WHERE UserName='test' AND ProjectName='test';",
            "Fetch":True
        }
        response = client.post(URL, json=query, headers={'Referer': URL, 'X-CSRFToken': csrfToken, 'Id': Id})
        responseJson = response.json()
        self.assertFalse(responseJson['ErrorMsg'])
        self.assertFalse(responseJson['Result'])

    def testCreateTestProject(self):
        query = {
            "Query":"INSERT INTO Projects (UserName,ProjectName) VALUES ('test','test');",
            "Fetch":False
        }
        response = client.post(URL, json=query, headers={'Referer': URL, 'X-CSRFToken': csrfToken, 'Id': Id})
        responseJson = response.json()
        self.assertFalse(responseJson['ErrorMsg'])
        self.assertTrue(responseJson['Result'])

    def testQueryTestProjectAfterCreation(self):
        query = {
            "Query":"Select UserName,ProjectName FROM Projects WHERE UserName='test' AND ProjectName='test';",
            "Fetch":True
        }
        response = client.post(URL, json=query, headers={'Referer': URL, 'X-CSRFToken': csrfToken, 'Id': Id})
        responseJson = response.json()
        self.assertFalse(responseJson['ErrorMsg'])
        self.assertEqual(1, len(responseJson['Result']))

    def testDeleteTestProject(self):
        query = {
            "Query":"DELETE FROM Projects WHERE UserName='test' AND ProjectName='test';",
            "Fetch":False
        }
        response = client.post(URL, json=query, headers={'Referer': URL, 'X-CSRFToken': csrfToken, 'Id': Id})
        responseJson = response.json()
        self.assertFalse(responseJson['ErrorMsg'])
        self.assertTrue(responseJson['Result'])

    def testQueryTestProjectAfterDeletion(self):
        query = {
            "Query":"Select UserName,ProjectName FROM Projects WHERE UserName='test' AND ProjectName='test';",
            "Fetch":True
        }
        response = client.post(URL, json=query, headers={'Referer': URL, 'X-CSRFToken': csrfToken, 'Id': Id})
        responseJson = response.json()
        self.assertFalse(responseJson['ErrorMsg'])
        self.assertFalse(responseJson['Result'])

if __name__ == '__main__':
    unittest.main()