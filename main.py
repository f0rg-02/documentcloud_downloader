#!/usr/bin/env python3

# FUCK YOU PYTHON

from documentcloud import DocumentCloud
from multiprocessing import Process

import uuid
import argparse
import os

# I got lazy
output = ""
orgs = []

client = DocumentCloud("USERNAME", "PASSWORD")
client._get_tokens(client.username, client.password)
client._refresh_tokens(client.refresh_token)
client._set_tokens()

def search_documentcloud(search, orgs, titles):
    items = []

    client._refresh_tokens(client.refresh_token)
    client._set_tokens()

    try:
        obj_list = client.documents.search(search)
    except Exception as error:
        print("Error at search: {} ".format(error))

    for item in obj_list:
        items.append(item)

        if len(items) % 100 == 0:
            #print("In len: ", client.refresh_token) # Used to make sure the token was actually being refreshed
            print("Passing list of items to handler function.")

            try:
                final_list = []
                final_list = check_org(orgs, items, titles)

                if len(final_list) > 0:
                    handle_id(final_list)

                items.clear() # Clear list for next set of items
                client._refresh_tokens(client.refresh_token)
                client._set_tokens()
            except Exception as error:
                print("Error at passing list to the handler function {}".format(error))
                
                if len(final_list) > 0:
                    handle_id(final_list)

                items.clear() # Clear list for next set of items
                client._refresh_tokens(client.refresh_token)
                client._set_tokens()
                pass
        
    print("Checking for any items after loop is finished")
    if len(items) > 0:
        try:
            final_list = []
            final_list = check_org(orgs, items, titles)

            if len(final_list) > 0:
                handle_id(final_list)

            items.clear() # Clear list for next set of items
            client._refresh_tokens(client.refresh_token)
            client._set_tokens()
        except Exception as error:
            print("Error at passing list to the handler function {}".format(error))
            
            if len(final_list) > 0:
                handle_id(final_list)

            items.clear() # Clear list for next set of items
            client._refresh_tokens(client.refresh_token)
            client._set_tokens()
            pass

def handle_list(list):    
    num_max = 10
    threads = []
    
    for item in list:
        obj = item
        print("[ID: {}] Getting document '{}' from '{}'".format(obj.id, obj.title, obj.canonical_url))
        p = Process(target=write_pdf, args=(obj, ))
        threads.append(p)

        if len(threads) == num_max:
            start_threads(threads)
            
            print("Finished processing items.")
            cleanup_threads(threads)
            threads.clear()
    
    if len(threads) > 0:
        start_threads(threads)
            
        print("Finished processing items.")
        cleanup_threads(threads)
        threads.clear()

def handle_id(list):    
    num_max = 10
    threads = []
    
    for item in list:
        obj = item
        p = Process(target=process_ids, args=(obj, ))
        threads.append(p)

        if len(threads) == num_max:
            start_threads(threads)
            
            print("Finished processing items.")
            cleanup_threads(threads)
            threads.clear()
    
    if len(threads) > 0:
        start_threads(threads)
            
        print("Finished processing items.")
        cleanup_threads(threads)
        threads.clear()

def check_title(keywords, items):
    buffer = list()
    for item in items:
        if len(keywords) != 0:
            for keyword in keywords:
                try:
                    if keyword in item.title:
                        print("Found document: {}".format(item.title))
                        item_id = item.id
                        buffer.append(item_id)
                except:
                    pass
        else:
            buffer.append(item.id)
           
    return buffer

# Some of the document titles have dashes where spaces are which don't get properly processed with the keywords
def format_title(titles):
    results = list()

    try:
        for title in titles:
            result = "-".join(title.split()) 
            results.append(result)

    except Exception as error:
        print("Error at format_title(): {}".format(error))

    return results

def check_org(orgs, items, keywords):
    buffer = list()
    chk_items = list()

    num_max = 10
    threads = []

    for item in items:
        if len(orgs) != 0:
            for org in orgs:
                try:
                    if org in item.contributor_organization:
                        chk_items.append(item)
                except:
                    pass
        else:
            chk_items.append(item)

    if len(chk_items) != 0:
        titles = format_title(keywords)
        
        for title in titles:
            keywords.append(title) 
        
        buffer = check_title(keywords, chk_items)
    
    return buffer

def cleanup_threads(threads):
    print("Cleaning up threads.")
    for thread in threads:
        thread.terminate()

def start_threads(threads):
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

def write_pdf(obj):

    try:
        if len(orgs) > 0:
            for org in orgs:
                try:
                    if org in obj.contributor_organization:
                        directory = output+"/"+org+"/"
                except:
                    pass
        else:
            directory = output+"/"

            fd = open(directory+str(uuid.uuid4())+".pdf", "wb")
            fd.write(obj.pdf)
            fd.close()
    except Exception as error:
        print("Error in writing to pdf: {}".format(error))

def process_ids(id):
    obj_list = []
    obj = client.documents.get(id)
    obj_list.append(obj)

    handle_list(obj_list)

def read_file(file):
    try:
        # Read file using readlines
        fd = open(file, 'r')
        lines = fd.readlines()
 
        return lines
    except Exception as error:
        print("Error at read_file: {}".format(error))

def parse_multi(arg_string):
    # Bad error handling, but I honestly don't see how this could fail
    try:
        arg_string = [s.strip() for s in arg_string.split(",")]
    except Exception as error:
        print("Error splitting the argument: {}".format(error))

    if arg_string is not None:
        return arg_string
    else:
        return ""

def chk_directories(dir):
    try:
        chk_exist = os.path.exists(dir)
    except Exception as error:
        print("Error at chk_directories() with trying to check if the directory exists: {}".format(error))

    if not chk_exist:
        try:
            os.makedirs(dir)
        except Exception as error:
             print("Error at chk_directories() with trying to create the directory: {}".format(error))   

def main():

    # Why can't you be normal python?
    global orgs
    global output
    
    searches = []
    titles = []


    parser=argparse.ArgumentParser(description="Simple python3 program to search and download documents from DocumentCloud.")
    parser.add_argument("--organizations", "-o", help="Specify an organization(s) to filter and narrow down documents that should be downloaded.", type=str)
    parser.add_argument("--org-file", "-of", help="File with a list of organizations to check for.")
    parser.add_argument("--search", "-s", help="Keyword(s) to search for documents on DocumentCloud.", type=str)
    parser.add_argument("--search-file", "-sf", help="File containing keywords to search for documents on DocumentCloud.")
    parser.add_argument("--filter-title", "-ft", help="Keyword(s) to filter based on title.", type=str)
    parser.add_argument("--title-file", "-tf", help="File containing Keyword(s) to filter based on title.", type=str)
    parser.add_argument("--output", "-od", help="Directory where to save the results to.", type=str)
    args=parser.parse_args()

    if args.organizations is not None:
        results = parse_multi(args.organizations)

        for org in results:
            orgs.append(org)

    elif args.org_file is not None:
        lines = read_file(args.org_file)
        
        for line in lines:
            orgs.append(line.strip())

    if args.search is not None:
        results = parse_multi(args.search)

        for search in results:
           searches.append('"{0}"'.format(search))
    elif args.search_file is not None:
        lines = read_file(args.search_file)

        for line in lines:
            searches.append('"{0}"'.format(line.strip()))
    
    if args.filter_title is not None:
        results = parse_multi(args.filter_title)

        for title in results:
            titles.append(title)
    elif args.title_file is not None:
        lines = read_file(args.title_file)

        for title in lines:
            titles.append(title)

    if args.output is not None:
        output = args.output
        
        if len(orgs) > 0:
            for org in orgs:
                chk_directories(output+"/"+org)
        else:
            chk_directories(output)
        
    else:
        output = os.path.abspath(os.getcwd())
        chk_directories(output)

    client._set_tokens()
    
    for search in searches:
        search_documentcloud(search, orgs, titles)

if __name__ == "__main__":
    main()

