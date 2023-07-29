from bs4 import BeautifulSoup as bs

class Explainer(object):
    def __init__(self) -> None:
        self.xmlParser = None
        self.data = None
        self.arithmeticDes = None
    def load(self,path):
        with open(path, 'r', encoding='utf-8') as f:
            self.data = f.read()
        self.xmlParser = bs(self.data, 'xml')

    def extractArithmeticDes(self):
        self.arithmeticDes =  self.xmlParser.find_all('arithemticOperations')
    
    def explainArithmetic(self, op ,kind, descriptionType , *args):
        description = str(self.arithmeticDes[0].find_all(op,{'kind':kind,'descriptionType':descriptionType})[0].contents[0])
        for arg,i in zip(args,range(len(args))):
           description =  description.replace(r'{arg'+str(i)+r'}',str(arg))
           
        return  description
