import web
import xml.etree.ElementTree as ET

tree = ET.parse('Ports.xml')
root = tree.getroot()

urls = (
	'/seaports', 'list_seaports',
	'/seaport/(.*)', 'get_seaport'
)

app = web.application(urls, globals())

class list_seaports:        
	def GET(self):
		output = 'seaports:['
		for child in root.findall("Port"):
			print ('child', child.tag, child.attrib)
			output += str(child.attrib) + ','
		output += ']'
		return output

class get_seaport:
	def GET(self, seaport):
		for child in root.findall("./Port/[id='"+seaport+"']"):
			return child.itertext()

if __name__ == "__main__":
	app.run()
	