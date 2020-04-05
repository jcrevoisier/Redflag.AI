# Coding assignment Redflag.ai
	
## DESCRIPTION

Server running programm (Flask) containing two endpoints :
	/ The crawler : Crawls 5 pictures on instagram based on a keyword, classify the pictures based on ResNet-50 model trained on ImageNet, and return classes with confidence as json
	/ The upload : Classify a pictures based on ResNet-50 model trained on ImageNet, and return class with confidence as json

## FILES
	server.py : Flask Module
		/ crawl() : Crawl endpoint
		/ upload() : Upload endpoint
		
	crawler.py : Crawler Module
		/ crawl(keyword) : Run crawler
		/ download_pictures() : Store pictures locally
		
	model.py : ML model Module
		/ set_crawl() : Set mode to crawler
		/ set_upload(img_path) : Set mode to upload
		/ run() : Run the model and return JSON of predictions
		
## PRE-REQUISITES
	/ Python modules to be installed on server side : flask, pyquery, requests, numpy, pandas, tensorflow==2.0
	
## HOW TO RUN

0) Download following scripts in the same repository 
	server.py / crawler.py / model.py
	
1) Launch the server
	command : python server.py
	
2) Launch a crawling
	command (client side) : curl http://localhost:5000/crawl?keyword=YOUR_KEYWORD (replace YOUR_KEYWORD)
	return json with predicted class for each picture
	
3) Launch an upload 
	command (client side) : curl http://localhost:5000/upload?file=YOUR_IMAGE (replace YOUR_IMAGE with image path)
	return json with predicted class

## RESULT

The JSON response will respect the following pattern :

	{
	'image_path' : 
		{
		'0' : ...
		'1' : ... 
		...
		'n' : ... 
		}
	'prediction' :
		{
		'0' : ...
		'1' : ...
		...
		'n' : ...
		}
	'confidence' :
		{
		'0' : ...
		'1' : ...
		...
		'n' : ...
		}
	}
