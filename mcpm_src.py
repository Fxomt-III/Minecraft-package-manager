import requests
import json
from pprint import pprint
import os
from sys import argv as a
import re

def cur_dir():
    return __file__.replace('\\', '/')[::-1].split('/', 1)[1][::-1]

data_json = json.loads(open(f'{cur_dir()}/data.json').read())

def link(wanted):
    return f'https://api.modrinth.com/v2/{wanted}'


def load_mod_page(urllink):
    urllink = link("project/"+urllink)
    url = requests.get(urllink)
    if url.ok:
        data = json.loads(url.content)
        data_display = data['title'] + ' ' + data['project_type']
        print('+'+'-'*(len(data_display)+2)+'+')
        print('| ' + data_display + ' |')
        print('+'+'-'*(len(data_display)+2)+'+\n')

        print(data['description'])
        print(
            f"\nThe {data_display} was published on {data['published']}, and was last updated on {data['updated']},\nit has {data['downloads']} downloads and has {data['followers']} followers.")
        print("\nCategories:")
        for i in data['categories']:
            print('    ' + i)
            
        print("\nWays to donate:")
        for i in data['donation_urls']:
            print(f'    {i["platform"]}: {i["url"]}')
        print('\n\n-- DATA  --------------------------------')
        print(f"License: {data['license']['name']}")
        print(f"Serverside: {data['server_side']}")
        print(f"Clientside: {data['client_side']}")
        print('\n\n-- LINKS --------------------------------')
        print(f'Source: {data["source_url"]}')
        print(f'Discord: {data["discord_url"]}')
        print(f'Wiki: {data["wiki_url"]}')
        

        if input("Print out the raw data? Y/N ").lower() == 'y':
            pprint(data)
    else:
        print("Page does not exist.")


def download_jar_mod(urllink, dir):
    urllink = link(f'project/{urllink.lower()}')

    url = requests.get(urllink)
    if url.ok:
        print("url response okay.")
        data = json.loads(url.content)
        mod_id = data['id']

        versions = json.loads(requests.get(
            f"https://api.modrinth.com/v2/project/{mod_id}/version").content)
        print("Fetched versions.")
        version_jar = versions[0]['files'][0]
        url = requests.get(version_jar['url']).content
        print("Got the link.")
        filename = version_jar['filename']

        data_json = json.loads(open(f'{cur_dir()}/data.json').read())
        print("Changing directory now...")
        cdir = os.getcwd()

        os.chdir(data_json['directories'][dir])
        print(f"Changed to {data_json['directories'][dir]}")
        print("Writing mod now...")
        with open(f'{data_json["directories"][dir]}/{filename}', 'wb') as f:
            f.write(url)
        print("Done! mod has been installed.")

        os.chdir(cdir)

        with open(f'{cur_dir()}/installed.json', 'r+') as f:
            _data = json.load(f)
            _data[dir].update({re.sub('\s+', '-', data['title'].lower()): filename})
            f.seek(0)
            json.dump(_data, f, indent=4)
            f.truncate()

    else:
        print("Mod does not exist.")


def remove_mod(name, dir):
    with open(f'{cur_dir()}/installed.json', 'r+') as f:
        text = f.read()
        data = json.loads(text)
        
        real_name = data[dir][name]
        cwd = os.getcwd()
        os.chdir(data_json['directories'][dir])
        os.remove(real_name)
        print(f"Deleted mod {name}.")

        os.chdir(cwd)

        _data = json.loads(text)
        _data[dir].pop(name.lower())
        f.seek(0)
        json.dump(_data, f, indent=4)
        f.truncate()


def add_mod_dir(dirname, dir):
    with open(f'{cur_dir()}/data.json', 'r+') as f:
        data = json.load(f)
        data['directories'][dirname] = dir
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    with open(f'{cur_dir()}/installed.json', 'r+') as f:
        data = json.load(f)
        data[dirname] = {}
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def list_mods(dir):
    with open(f'{cur_dir()}/installed.json', 'r') as f:
        data = json.loads(f.read())[dir]
        print(f"--- {dir} mods ---")
        for modname, _ in data.items():
            print(f"{modname}")

def check_mod(name, dir):
    with open(f'{cur_dir()}/installed.json', 'r') as f:
        data = json.loads(f.read())[dir]
        if name in data:
            print("Mod exists.")
        else:
            print("Mod does not exist.")

# mcpm install sodium fabric-18.2
# mcp  <CMD> <MOD> <DIR>

def usage():
    print("Usage: <CMD> [MOD] <DIR>")
    print("Commands:")
    print("    install - install a mod")
    print("    list    - show all installed mods")
    print("    check   - check if mod is installed")
    print("    remove  - remove a mod")
    print("    add     - add a directory")
    print("    info    - show info about a mod")
    print("Mod is the name of the wanted mod,")
    print("and dir is the wanted directory.")


if len(a) <= 2:
    usage()

def get_mod_arg():
    if len(a) <= 3:
        usage()
        return
    return a[2]

def get_dir_arg():
    if len(a) <= 3:
        usage()
        return
    return a[3]

cmd = a[1].lower()


if cmd == 'install':
        download_jar_mod(get_mod_arg(), get_dir_arg())
elif cmd == 'list':
        list_mods(a[2])
elif cmd == 'check':
        check_mod(get_mod_arg(), get_dir_arg())
elif cmd == 'remove':
        remove_mod(get_mod_arg(), get_dir_arg())
elif cmd == 'add':
        add_mod_dir(get_mod_arg(), get_dir_arg())
elif cmd == 'info':
        load_mod_page(a[2])