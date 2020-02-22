import os,re,xml.sax

path=""
pathList=[]

class Traverser:
	#This fuction will travers the given folder structure and list down the xml files with name in the format "data-xxxxx.xml"
	def traverse(self):
		fileList=[]
		xmlPath=input("Enter the path: ")
		for root, dirs, files in os.walk(xmlPath, topdown=False):
			for name in files:
				if(name.startswith("data-") and name.endswith(".xml")):
					fileList.append(os.path.join(root, name))
					pathList.append(os.path.join(root,""))		
		return fileList
		
#This class reads xml and writes the values to the CSV file
class CSVGen(xml.sax.ContentHandler):
	def __init__(self):
		self.CurrentData=""
		self.uid=""
		self.title=""
		self.actor=""
		self.director=""
		self.country=""
		self.asset=""
		self.format=""
		self.bitrate=""
		if os.path.exists("xmltocsv.csv"):
			os.remove("xmltocsv.csv")
		
	# Call when an element starts
	def startElement(self, tag, attributes):
		self.CurrentData = tag
		if tag == "product":
			self.uid = attributes["uid"]
			self.csv(self.uid)
	
	# Call when an elements ends
	def endElement(self, tag):
		if self.CurrentData == "title":
			self.csv(self.title)
		elif self.CurrentData == "actor":
			self.csv(self.actor)
		elif self.CurrentData == "director":
			self.csv(self.director)
		elif self.CurrentData == "country":
			self.csv(self.country)
		elif self.CurrentData == "format":
			self.csv(self.format)
		elif self.CurrentData == "bitrate":
			self.csv(self.bitrate)
		elif self.CurrentData == "fps":
			self.csv(self.fps)
		elif self.CurrentData == "aspect":
			self.csv(self.aspect)	
		elif self.CurrentData == "width":
			self.csv(self.width)
		self.CurrentData = ""
		
	# Call when a character is read
	def characters(self, content):
		if self.CurrentData == "title":
			self.title = content
		elif self.CurrentData == "actor":
			self.actor = content
		elif self.CurrentData == "director":
			self.director = content
		elif self.CurrentData == "country":
			self.country = content
		elif self.CurrentData == "format":
			self.format = path+self.uid+"\\"+content
		elif self.CurrentData == "bitrate":
			self.bitrate = content
		elif self.CurrentData == "fps":
			self.fps = content
		elif self.CurrentData == "aspect":
			self.aspect = content
		elif self.CurrentData == "width":
			self.width = content

	# Writes data to a CSV file
	def csv(self,s):
		f=open("xmltocsv.csv",'a')
		f.write(s)
		f.write(",")
		 
if ( __name__ == "__main__"):
	t = Traverser()
	fileList = t.traverse()
	# create an XMLReader
	parser = xml.sax.make_parser()
	# turn off namepsaces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = CSVGen()
	parser.setContentHandler(Handler)
	for (file,thispath) in zip(fileList,pathList):
		path=thispath
		parser.parse(file)
	
