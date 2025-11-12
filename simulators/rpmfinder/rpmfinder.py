import subprocess
from bs4 import BeautifulSoup
import urllib.parse
import os

def install_package(local_path):
    command = ["dnf", "install", local_path, "-y"]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    if process.returncode == 0:
        print(f"Installation successful from local path: {local_path}")
        return True
    else:
        print(f"Installation failed from local path: {local_path}.")
        print(process.stderr)
        return False

def fetch_html_content(package_name):
    encoded_package_name = urllib.parse.quote(package_name)
    search_url = f"https://rpmfind.net/linux/rpm2html/search.php?query={encoded_package_name}&submit=Search+...&system=&arch="
    temp_file_path = "/tmp/rpmfind_search.html"
    subprocess.run(["wget", "-q", "-O", temp_file_path, search_url])
    
    with open(temp_file_path, 'r') as file:
        html_content = file.read()
    
    os.remove(temp_file_path)
    return html_content

def filter_results(html_content, rhel_ver):
    soup = BeautifulSoup(html_content, 'html.parser')
    filtered_url = None
    current_ver = int(rhel_ver)

    # Loop until a URL is found or the version number becomes too low
    while not filtered_url and current_ver > 0:
        search_text = f"EPEL {current_ver} for x86_64"
        epel_results = soup.find_all('td', text=search_text)
        for result in epel_results:
            link_tag = result.find_next('td').find('a')
            if link_tag:
                filtered_url = link_tag['href']
                break
        current_ver -= 1  # Decrement version number if no URL was found

    return filtered_url

def download_package(relative_url, save_directory):
    base_url = "https://rpmfind.net"
    full_url = base_url + relative_url
    file_name = full_url.split('/')[-1]
    full_path = os.path.join(save_directory, file_name)
    subprocess.run(["wget", full_url, "-O", full_path])
    print(f"Package downloaded and saved to: {full_path}")
    return full_path

def main():
    package_name = "armadillo"
    download_directory = "/home/caleb/files"
    rhel_ver = "8"

    html_content = fetch_html_content(package_name)
    filtered_url = filter_results(html_content, rhel_ver)
    
    if filtered_url:
        print(f"Downloading package from: {filtered_url}")
        downloaded_file_path = download_package(filtered_url, download_directory)
        # Try installing the downloaded package
        install_package(downloaded_file_path)
    else:
        print("No appropriate package found for any version of EPEL for x86_64.")

if __name__ == "__main__":
    main()
