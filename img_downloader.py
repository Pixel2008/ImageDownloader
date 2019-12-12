#! python3

'''
Sample script for downloading all images from website
Pixel2008 All Rights Reserved ®
'''
from typing import List
import sys, requests, bs4, traceback, os, shutil

def get_url() -> str:
    def_url = "www.google.pl"
    url = input("Enter url address [press enter key for default url " + def_url + "]: ")
    if len(url) == 0:
        return def_url   
    return url

# Simple parsing
def check_url(url : str) -> bool:
    if len(url) == 0:
        return False
    return True

def get_img_links(url : str) -> List:    
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,"html.parser")
    images = soup.select("img")
    if images == []:
        print("Couldn't find any img!")
        return list()
    lst = []
    for img in images:
        lst.append(img.get("src"))
    return lst

def prepare_download_dir(start_dir : str) -> str:
    path = os.path.join(start_dir,"tmp_download")   
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path

def download_all_images(img_links: List, download_path : str):   
    #print(img_links) 
    allowed_extensions = ("png","jpg","jpeg")
    counter = 0
    for img in img_links:        
        url = img        
        name = img[img.rfind("/")+1:]
        ext = img[img.rfind(".")+1:].lower()
        if ext not in allowed_extensions:
            continue

        if not url.startswith('http'):
            url = "http:" + img
        
        print("Downloading",name,url)        
        try:
            res = requests.get(url)
            res.raise_for_status()
        
            imageFile = open(os.path.join(download_path,name),'wb')
            try:
                for chunk in res.iter_content(1024):
                    imageFile.write(chunk)            
                counter += 1
            finally:
                imageFile.close()
        except requests.exceptions.InvalidURL:
            print("Invalid url",url)
            continue
        except:
            print("Error while downloading")
            continue
    return counter

def get_top_10(download_path : str):
    all_files = []
    for (path, _, files) in os.walk(download_path):
        for file in files:
            size = os.path.getsize(os.path.join(path,file))
            all_files.append((os.path.join(path,file), size))
    all_files.sort(key=lambda x:x[1])
    return all_files[0:10]

def mail_images(top_ten_imaes: List):
    '''
        python_test_01@int.pl
        python_test_02@int.pl
        imap/smtp poczta.int.pl
        IMAP: 143 (TLS)
        SMTP: 465 (TLS)
    '''
    pass

if __name__ == "__main__":
    try:
        #clear consloe
        clear = lambda: os.system("cls")
        clear()


        # url
        url = get_url()

        # parse
        if not check_url(url):
            print("Bad url! Quiting!")
            sys.exit(1)

        # get img links
        img_links = get_img_links(url)
                
        # prepare dirs
        start_path = os.path.dirname(os.path.realpath(__file__))
        download_path = prepare_download_dir(start_path)

        # download all in multiple threads
        downloaded = download_all_images(img_links,download_path)
        print("Downloaded",downloaded,"images")

        # get top 10 lowest size
        top_10_lowest = get_top_10(download_path)
        print("Lowest size images",top_10_lowest)

        # send them by mail
        mail_images(top_10_lowest)
        
        # prepare mail dirs

        # receive mail

    except requests.exceptions.MissingSchema as e1:
        print("Error occured e1 = " + format(e1))
        print("Call stack:")
        traceback.print_tb(e1.__traceback__)
    except Exception as e2:
        print("Error occured e2 = " + format(e2))
        
        
