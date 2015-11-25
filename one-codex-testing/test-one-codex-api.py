#!/usr/bin/env python
"""
client.py
author: Kyle McChesney
Toying around with Potion Client
"""
from potion_client import Client

def main():

    # takes base url and schema addition
    client = Client(base_url="http://localhost:5000", schema_path="/api/potion/schema")
    Files = client.File
    Tags = client.Tag

    files = Files.instances
    print files

    default_tags = Tags.instances.where(is_default = True)
    print default_tags
    
    t = Tags()
    t.name = "test"
    t.save()


if __name__ == "__main__":
    main()