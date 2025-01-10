import requests
import os
import zipfile
import shutil
from dotenv import load_dotenv

load_dotenv()
baseURL='https://www.curseforge.com/api/v1/mods/462042/files'
temp_dir='new_version'

my_java_args=os.getenv('JAVA_ARGS')
custom_motd=os.getenv('MOTD')
minecraft_folder = os.getenv('MINECRAFT_FOLDER')

def getServerFileId():
    response = requests.get(f'{baseURL}?pageIndex=0&pageSize=20&sort=dateCreated&sortDescending=true&removeAlphas=true')
    if response.status_code == 200:
        data_latest = response.json()['data'][0]
        if(data_latest['releaseType']==1 and data_latest['hasServerPack']==True):
            id=data_latest['id']
            addtionalFile=requests.get(f'{baseURL}/{id}/additional-files')
            if(addtionalFile.status_code==200):
                serverFileId=addtionalFile.json()['data'][0]['id']
                return serverFileId
            else:
                print(f"Error: {addtionalFile.status_code}")    
        else:
            print("No server pack found")
            exit()
    else:
        print(f"Error: {response.status_code}")
def getServerFile(serverFileId):
    print('Downloading File')
    filename = f'server_{serverFileId}.zip'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(f'{baseURL}/{serverFileId}/download', headers=headers, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return filename
    else:
        print(f"Error: {response.status_code}")
        return None       
def extract_server_files(zip_filename):
    # Create temp directory if it doesn't exist
    if os.path.exists(temp_dir):
        # Clean up existing temp directory
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    try:
        # Extract the zip file
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        print(f"Files extracted successfully to {temp_dir} directory")
        return True
    except zipfile.BadZipFile:
        print("Error: The downloaded file is not a valid zip file")
        return False
    except Exception as e:
        print(f"Error extracting files: {str(e)}")
        return False
def update_java_args(new_args):
    filepath = os.path.join(temp_dir, 'variables.txt')
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    try:
        # Read the file content
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        # Create new content with updated JAVA_ARGS
        new_content = []
        found = False
        for line in lines:
            if line.startswith('JAVA_ARGS='):
                new_content.append(f'JAVA_ARGS="{new_args}"\n')
                found = True
            else:
                new_content.append(line)
        
        # Write the updated content back to file
        with open(filepath, 'w') as file:
            file.writelines(new_content)
            
        print(f"Successfully updated JAVA_ARGS to: {new_args}")
        return True
        
    except Exception as e:
        print(f"Error updating JAVA_ARGS: {str(e)}")
        return False
def update_server_properties():
    filepath = os.path.join(temp_dir, 'server.properties')
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    try:
        # Read the file content
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        # Create new content with updated properties
        new_content = []
        properties_updated = {'online-mode': False, 'white-list': False, 'motd': False}
        
        for line in lines:
            # Skip comments and empty lines
            if line.strip().startswith('#') or not line.strip():
                new_content.append(line)
                continue
                
            if line.startswith('online-mode='):
                new_content.append('online-mode=false\n')
                properties_updated['online-mode'] = True
            elif line.startswith('white-list='):
                new_content.append('white-list=true\n')
                properties_updated['white-list'] = True
            elif line.startswith('motd='):
                new_content.append(f'motd={custom_motd}\n')
                properties_updated['motd'] = True
            else:
                new_content.append(line)
        
        # Add any properties that weren't found
        if not properties_updated['online-mode']:
            new_content.append('online-mode=false\n')
        if not properties_updated['white-list']:
            new_content.append('white-list=true\n')
        if not properties_updated['motd']:
            new_content.append(f'motd={custom_motd}\n')
        
        # Write the updated content back to file
        with open(filepath, 'w') as file:
            file.writelines(new_content)
            
        print("Successfully updated server.properties:")
        print(f"- online-mode set to false")
        print(f"- white-list set to true")
        print(f"- motd set to: {custom_motd}")
        return True
        
    except Exception as e:
        print(f"Error updating server.properties: {str(e)}")
        return False
def update_parties_and_claims_config():
    filepath = os.path.join(temp_dir, 'config', 'openpartiesandclaims-server.toml')
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    try:
        # Read the file content
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        # Create new content with updated settings
        new_content = []
        in_parties_section = False
        in_claims_section = False
        
        for line in lines:
            # Track which section we're in
            if "[serverConfig.parties]" in line:
                in_parties_section = True
                in_claims_section = False
            elif "[serverConfig.claims]" in line:
                in_parties_section = False
                in_claims_section = True
                
            # Update the enabled setting in the appropriate section
            if "enabled = " in line:
                if in_parties_section or in_claims_section:
                    new_content.append('\t\tenabled = false\n')
                else:
                    new_content.append(line)
            else:
                new_content.append(line)
        
        # Write the updated content back to file
        with open(filepath, 'w') as file:
            file.writelines(new_content)
            
        print("Successfully updated openpartiesandclaims-server.toml:")
        print("- Disabled parties")
        print("- Disabled claims")
        return True
        
    except Exception as e:
        print(f"Error updating openpartiesandclaims-server.toml: {str(e)}")
        return False
def create_eula():
    eula_content = """#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).
eula=true"""
    try:
        # Create eula.txt in the temp directory
        with open(os.path.join(temp_dir, 'eula.txt'), 'w') as file:
            file.write(eula_content)
        print("Successfully created eula.txt with agreement set to true")
        return True
    except Exception as e:
        print(f"Error creating eula.txt: {str(e)}")
        return False
def copy_server_files():
    if not minecraft_folder:
        print("Error: MINECRAFT_FOLDER not set in environment variables")
        return False

    files_to_copy = {
        'whitelist.json': 'whitelist.json',
        'server-icon.png': 'server-icon.png'
    }

    success = True
    for source_file, dest_file in files_to_copy.items():
        source_path = os.path.join(minecraft_folder, source_file)
        dest_path = os.path.join('temp', dest_file)

        try:
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
                print(f"Successfully copied {source_file} to temp directory")
            else:
                print(f"Warning: {source_file} not found in {minecraft_folder}")
                success = False
        except Exception as e:
            print(f"Error copying {source_file}: {str(e)}")
            success = False

    return success  
   

if __name__ == "__main__":
    serverFileId = getServerFileId()
    zip_filename = getServerFile(serverFileId)
    
    if zip_filename:
        print("Server file downloaded successfully.")
        if extract_server_files(zip_filename):
            # Optionally remove the zip file after extraction
            os.remove(zip_filename)
            print(f"Removed zip file: {zip_filename}")
        else:
            print("Failed to extract server files.")
        update_java_args(my_java_args)
        update_server_properties()
        update_parties_and_claims_config()
        create_eula()
        copy_server_files()
    else:
        print("Failed to download server file.")