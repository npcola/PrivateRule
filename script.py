import requests

def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def read_local_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def merge_and_deduplicate(contents, local_content):
    # 合并网页内容和本地文件内容
    combined = '\n'.join(contents + [local_content])
    unique_lines = set(combined.splitlines())
    return '\n'.join(unique_lines)

def remove_specified_lines(contents):
    # 删除以“!”和“[”开头的行
    return '\n'.join([line for line in contents.splitlines() if not (line.startswith('!') or line.startswith('['))])

def save_to_file(contents, file_name):
    with open(file_name, 'w') as file:
        file.write(contents)

def main():
    # 读取URLs
    urls = read_urls('./rules/url.txt')
    
    # 存储所有网页内容
    contents = []
    
    # 下载并合并网页内容
    for url in urls:
        content = fetch_content(url)
        if content:
            contents.append(content)
    
    # 读取本地文件内容
    local_content = read_local_file('./rules/other.txt')
    
    # 合并网页内容和本地文件内容，并去重
    combined_content = merge_and_deduplicate(contents, local_content)
    
    # 删除以“!”和“[”开头的行
    filtered_content = remove_specified_lines(combined_content)
    
    # 保存到新文件
    save_to_file(filtered_content, 'Private Rule.txt')
    print("Merged and filtered content has been saved to 'Private Rule.txt'.")

if __name__ == "__main__":
    main()