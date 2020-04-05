###############################################################################
##                                 Crawler                                   ##
##                                                                           ##
##      Crawl up to 5 images found on Instagram by keyword search            ##
##                                                                           ##
##          - Keyword to be pass as an argument                              ## 
##          - Pictures downloaded in 'download_path' (see config section)    ##                
##                                                                           ## 
###############################################################################

import os
import urllib
import requests
import pyquery
import json
import re

class Crawler :
    
    ######################
    ####### CONFIG #######
    ######################
    
    pictures = []
    nb_pictures = 5
    download_path = 'pictures//'

    ######################
    ####### CRAWL ########
    ######################

    def crawl(self, keyword):
        url = 'https://www.instagram.com/explore/tags/' + keyword
        self.pictures = [] #Reinitialize the list for every new crawl
        count = 0
        
        # Extract javascripts from the instagram URL
        xml = pyquery.PyQuery(url)
        items = xml("script[type='text/javascript']").items()
        
        # Retrieve pictures from the javascript
        content_start = 'window._sharedData = '
        for item in items:
            if item.text().strip().startswith(content_start):
                json_content = json.loads(item.text()[len(content_start):-1], encoding='utf-8')
                edges = json_content['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        
        # Append nb_pictures pictures to our list
        for edge in edges:
            if(count == self.nb_pictures):
                break
            
            # Extract json shortcode of the image
            url_shortcode = 'https://www.instagram.com/p/' + edge['node']['shortcode'] + '/?__a=1'
            with urllib.request.urlopen(url_shortcode) as temp_u:
                json_data = json.loads(temp_u.read().decode())
                
            # Select and extract the image ('GraphImage')
            if json_data['graphql']['shortcode_media']['__typename'] == 'GraphImage':
                display_url = json_data['graphql']['shortcode_media']['display_url']
                self.pictures.append(display_url)
                count += 1
    
    ######################
    ## DOWNLOAD PICTURES #
    ######################

    def download_pictures(self):
        # Create download directory
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        
        # Download pictures
        for i in range(0,len(self.pictures)):
            picture_path = self.download_path + 'picture_' + str(i) + '.png'             
            try:
                urllib.request.urlretrieve(self.pictures[i], picture_path)
            except urllib.error.HTTPError as err:
                print(pictures[i],' downloading fail... Error code: ',err.code)