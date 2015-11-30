#!/usr/bin/env python
"""
client.py
author: Kyle McChesney
Toying around with Potion Client
"""
from potion_client import OneCodexClient

def main():

    # takes base url and schema addition
    client = OneCodexClient(base_url="http://localhost:5000", schema_path="/api/potion/schema")

    # Initalize all the seperate models
    Sample = client.Sample

    test_sample = Sample.instances()[0]
    test_sample.download_file()

if __name__ == "__main__":
    main()