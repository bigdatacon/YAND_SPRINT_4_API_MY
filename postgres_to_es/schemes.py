import json

class Schemes:
    __schemes = None
    def get_schemes(self):
        if self.__schemes:
            return self.__schemes
        with open('schemes.json') as json_file:
            self.__schemes = json.load(json_file)
        return self.__schemes

# A = Schemes()
# print(A.get_schemes())