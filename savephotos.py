
 
import json
from decimal import Decimal

#Does quasi the same things as json.loads from here: https://pypi.org/project/dynamodb-json/
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


import subprocess
import wget

import pathlib
script_running_directory_path = pathlib.Path(__file__).parent.resolve()

import urllib.request 
import json
import os
from urllib.parse import urlparse
# Opening JSON file 
f = open('list.json')  
 
count = 0 

# returns JSON object as a list 
data = json.load(f)  

with open('outfile.json', 'w', encoding='utf-8') as outfile:
	outfile.write('[')
	for row in data:
		image_url = row['Image']  

		imageUrlParse = urlparse(image_url) 
		imageFilename = os.path.basename(imageUrlParse.path)
		imageFilenameExtension = os.path.splitext(imageFilename)[1]
		newImageFilename = (slugify(row['Name'] + ', '+row["Location"]) + imageFilenameExtension).lower() 
		saveFileNameAs = os.path.join(script_running_directory_path, "images", newImageFilename)
		referenceFileNameAs = os.path.join("images", newImageFilename)

		if os.path.exists(referenceFileNameAs): 
			row['Image'] = referenceFileNameAs
			row['Image_URL'] = image_url 





		if not os.path.exists(referenceFileNameAs): 

			# print(image_url)
			# print(imageFilename) 
			# print(saveFileNameAs)
			# print(referenceFileNameAs)

			# print("\n")


			try: 
				urllib.request.urlretrieve(image_url, saveFileNameAs)
				row['Image'] = referenceFileNameAs
				row['Image_URL'] = image_url 

			except: 

				try:  
					wget.download(image_url, saveFileNameAs) 

					row['Image'] = referenceFileNameAs
					row['Image_URL'] = image_url 

				except Exception as e:
					count+=1
					# print(count) 
					# print(image_url)
					# print(imageFilename) 
					# print(saveFileNameAs)
					# print(referenceFileNameAs)
					# print(e)  

					print("# " + str(count))

					print("wget -O " + saveFileNameAs + " \"" + image_url+ "\"")

					print("\n")
		 
					row['Image'] = referenceFileNameAs
					row['Image_URL'] = image_url 

		json.dump(row, outfile, ensure_ascii=False, indent=4, cls=JSONEncoder)
		outfile.write(',\n') 

	outfile.write(']')



