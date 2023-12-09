import requests
import PySimpleGUI as sg
from bs4 import BeautifulSoup
import wget
import os
from pathlib import Path
from patcher import run_command_gui
from path_all import paths


#Scrape API
def scrape_url():
    url = 'https://api.revanced.app/tools'
    r = requests.get(url).json()
    #pathces
    patches_url = r['tools'][1]['browser_download_url']
    patches_name = r['tools'][1]['name']
    #integrations
    integrations_url = r['tools'][2]['browser_download_url']
    integrations_name = r['tools'][2]['name']
    #cli
    cli_url = r['tools'][4]['browser_download_url']
    cli_name = r['tools'][4]['name']

    #return
    all_name_file = [cli_name,integrations_name, patches_name]
    all_url = [cli_url,integrations_url,patches_url]
    return all_url,all_name_file

#Download a File
def download_file(url,name):
    tools_folder = paths()[1]
    try: 
        #Download
        tools_file = os.path.join(tools_folder / name)

        wget.download(url,tools_file)
        
    except:
        print('ERROR')

def main_download():
    urls = scrape_url()[0]
    names = scrape_url()[1]
    #Download everything (for first startup)
    for url,name in zip(urls,names):
        download_file(url,name)

def check_update():
    all_url,all_name_file = scrape_url()
    tools_folder = paths()[1]
    folders = paths()
    #Create folders if they don't exist
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
    #Try: see if the folder tools have files, if not download everyting (for fist startup) 
    try:
        list_dir_tools = os.listdir(tools_folder)
        list_dir_tools[1]
    except IndexError as e:
        main_download()
    #Check update files, the name of the files is the same of the API REVANCED, so can compare the name, if the name is not the same
    #Is because is an update, so is goiung to remove the old file and download the new one
    try:
        for index, (file_name, scrape_name) in enumerate(zip(list_dir_tools, all_name_file)):
                if file_name != scrape_name:
                    sg.popup_auto_close(f"Update Avalible:\nActual: {file_name}\nNew: {scrape_name} ",auto_close_duration=4)
                    remove_file = os.path.join(tools_folder,file_name)
                    os.remove(remove_file)
                    download_file(all_url[index],all_name_file[index])
                elif file_name == scrape_name:
                    sg.popup_auto_close(f"Already updated:\nActual: {file_name}\nWEB: {scrape_name} ",auto_close_duration=2)
    except:
        print('HERE')

