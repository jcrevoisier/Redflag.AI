###############################################################################
##                                 Serveur                                   ##
##                                                                           ##
##      Flask application listening on localhost :                           ##
##                                                                           ##
##      Two endpoints :                                                      ##
##                                                                           ##                 
##          '/crawl' :  Search via crawler by keyword on instagram           ## 
##                       and return ML analysis of 5 first pictures          ##
##                                                                           ##
##          '/upload' :  Upload 1 image and get the ML analysis              ## 
##                                                                           ## 
###############################################################################

from crawler import Crawler
from model import Model
from flask import Flask, request, jsonify

######################
####### CONFIG #######
######################

app = Flask(__name__)
model_1 = Model()
 
######################
### CRAWL COMMAND ####
######################

@app.route('/crawl')
def crawl():
    # Retrieve keyword
    keyword = request.args['keyword']
    
    # Run the crawler
    crawler_1 = Crawler()
    crawler_1.crawl(keyword)
    crawler_1.download_pictures()
    
    # Run the model
    model_1.set_crawl()
    prediction = model_1.run()

    return prediction

######################
### UPLOAD COMMAND ###
######################

@app.route('/upload')
def upload():
    # Retrieve image path
    file = request.args['file']
    
    # Run the model
    model_1.set_upload(file)
    prediction = model_1.run()

    return prediction
  
######################
######## MAIN ########
######################
  
if __name__ == '__main__':
    app.run(debug=True, threaded=False)