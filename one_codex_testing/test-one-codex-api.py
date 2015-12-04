#!/usr/bin/env python
"""
client.py
author: Kyle McChesney
Toying around with Potion Client
"""
from potion_client import Client

def main():

    # takes base url and schema addition
    extensions = [SampleExtension]
    client = Client(base_url="http://localhost:5000", schema_path="/api/potion/schema", extensions=extensions)

    # Initalize all the seperate models
    Sample = client.Sample
    test_sample = Sample.instances()[0]
    test_sample.download_file()

class SampleExtension(object):
    
    resource = "Sample"

    def download_file(self):
        print "I am an awesome extension function"
        print "Downloading: {}".format(self.uri)

if __name__ == "__main__":
    main()