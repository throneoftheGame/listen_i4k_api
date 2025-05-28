#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载链接提取器
从API抓取日志中提取真实的下载链接并验证可用性
"""

import json
import os
import requests
import urllib.parse
from datetime import datetime
from colorama import init, Fore, Style
import re

# 初始化colorama
init()

class DownloadLinkExtractor:
    def __init__(self):
        self.download_links = []
        
    def extract_from_logs(self, log_directory="logs"):
        """从日志文件中提取下载链接"""
        print(f"{Fore.GREEN}🔍 开始从日志中提取下载链接{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        if not os.path.exists(log_directory):
            print(f"{Fore.RED}❌ 日志目录不存在: {log_directory}{Style.RESET_ALL}")
            return []
        
        # 查找所有JSON日志文件
        json_files = [f for f in os.listdir(log_directory) if f.startswith('api_requests_') and f.endswith('.json')]
        
        if not json_files:
            print(f"{Fore.YELLOW}⚠️  未找到API请求日志文件{Style.RESET_ALL}")
            return []
        
        for json_file in json_files:
            file_path = os.path.join(log_directory, json_file)
            print(f"\n📄 分析文件: {json_file}")
            self._process_log_file(file_path)
        
        return self.download_links
    
    def _process_log_file(self, file_path):
        """处理单个日志文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for entry in data:
                if 'response' in entry and 'body' in entry['response']:
                    self._extract_download_urls(entry)
                    
        except Exception as e:
            print(f"{Fore.RED}❌ 读取文件失败 {file_path}: {str(e)}{Style.RESET_ALL}")
    
    def _extract_download_urls(self, entry):
        """从响应中提取下载URL"""
        try:
            response_body = entry['response']['body']
            request_url = entry['request']['url']
            
            # 检查是否是阿里云盘API响应
            if ('aliyun' in request_url and 'api.php' in request_url) or \
               ('aliyundrive' in str(response_body)):
                
                download_url = None
                file_info = {}
                
                # 解析JSON响应
                if isinstance(response_body, dict):
                    # 直接是字典格式
                    if 'url' in response_body:
                        download_url = response_body['url']
                        file_info = response_body
                elif isinstance(response_body, str):
                    # 尝试解析JSON字符串
                    try:
                        json_data = json.loads(response_body)
                        if 'url' in json_data:
                            download_url = json_data['url']
                            file_info = json_data
                    except:
                        # 可能是HTML或其他格式，尝试正则提取
                        url_pattern = r'https://[^"\'>\s]+aliyundrive\.net[^"\'>\s]*'
                        urls = re.findall(url_pattern, response_body)
                        if urls:
                            download_url = urls[0]
                
                if download_url and 'aliyundrive.net' in download_url:
                    link_info = {
                        'timestamp': entry['request']['timestamp'],
                        'request_url': request_url,
                        'download_url': download_url,
                        'file_info': file_info,
                        'query_params': entry['request'].get('query_params', {})
                    }
                    
                    self.download_links.append(link_info)
                    self._display_found_link(link_info)
                    
        except Exception as e:
            pass  # 跳过无法解析的响应
    
    def _display_found_link(self, link_info):
        """显示找到的下载链接"""
        print(f"\n{Fore.GREEN}✅ 发现下载链接{Style.RESET_ALL}")
        print(f"⏰ 时间: {link_info['timestamp']}")
        print(f"🔗 请求URL: {link_info['request_url']}")
        
        # 显示查询参数
        if link_info['query_params']:
            print(f"📋 请求参数:")
            for key, value in link_info['query_params'].items():
                print(f"   {key}: {value}")
        
        # 显示文件信息
        if link_info['file_info']:
            if 'type' in link_info['file_info']:
                print(f"📁 文件类型: {link_info['file_info']['type']}")
            if 'delfile' in link_info['file_info']:
                print(f"🗑️  删除状态: {link_info['file_info']['delfile']}")
        
        # 显示下载链接（截断显示）
        url = link_info['download_url']
        if len(url) > 100:
            display_url = url[:50] + "..." + url[-50:]
        else:
            display_url = url
        print(f"📥 下载链接: {display_url}")
        print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
    
    def verify_links(self):
        """验证下载链接的可用性"""
        print(f"\n{Fore.YELLOW}🔍 开始验证下载链接{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        for i, link_info in enumerate(self.download_links):
            print(f"\n📎 验证链接 {i+1}/{len(self.download_links)}")
            self._verify_single_link(link_info)
    
    def _verify_single_link(self, link_info):
        """验证单个下载链接"""
        url = link_info['download_url']
        
        try:
            # 发送HEAD请求检查链接状态
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            print(f"🔄 检查链接状态...")
            response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
            
            print(f"📊 状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ 链接有效！{Style.RESET_ALL}")
                
                # 显示文件信息
                if 'Content-Length' in response.headers:
                    size = int(response.headers['Content-Length'])
                    size_mb = size / (1024 * 1024)
                    print(f"📏 文件大小: {size_mb:.2f} MB")
                
                if 'Content-Type' in response.headers:
                    print(f"📄 文件类型: {response.headers['Content-Type']}")
                
                if 'Content-Disposition' in response.headers:
                    disposition = response.headers['Content-Disposition']
                    # 提取文件名
                    filename_match = re.search(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)', disposition)
                    if filename_match:
                        filename = filename_match.group(1).strip('"\'')
                        # URL解码文件名
                        try:
                            filename = urllib.parse.unquote(filename)
                        except:
                            pass
                        print(f"📁 文件名: {filename}")
                        
            elif response.status_code == 403:
                print(f"{Fore.YELLOW}⚠️  链接已过期或无权限访问{Style.RESET_ALL}")
            elif response.status_code == 404:
                print(f"{Fore.RED}❌ 文件不存在{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️  状态码: {response.status_code}{Style.RESET_ALL}")
                
        except requests.exceptions.Timeout:
            print(f"{Fore.YELLOW}⏰ 请求超时{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}❌ 请求失败: {str(e)}{Style.RESET_ALL}")
    
    def save_links_to_file(self, filename="extracted_download_links.json"):
        """保存提取的链接到文件"""
        if not self.download_links:
            print(f"{Fore.YELLOW}⚠️  没有找到下载链接{Style.RESET_ALL}")
            return
        
        output_data = {
            'extracted_time': datetime.now().isoformat(),
            'total_links': len(self.download_links),
            'links': self.download_links
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n{Fore.GREEN}💾 链接已保存到: {filename}{Style.RESET_ALL}")
            print(f"📊 总共提取了 {len(self.download_links)} 个下载链接")
            
        except Exception as e:
            print(f"{Fore.RED}❌ 保存失败: {str(e)}{Style.RESET_ALL}")
    
    def get_direct_download_url(self, aliyun_api_url):
        """直接从阿里云API获取下载链接"""
        print(f"\n{Fore.BLUE}🚀 尝试直接获取下载链接{Style.RESET_ALL}")
        print(f"🔗 API URL: {aliyun_api_url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*'
            }
            
            response = requests.get(aliyun_api_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'url' in data:
                        print(f"{Fore.GREEN}✅ 成功获取下载链接！{Style.RESET_ALL}")
                        return data['url']
                    else:
                        print(f"{Fore.YELLOW}⚠️  响应中没有找到下载链接{Style.RESET_ALL}")
                        print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
                except:
                    print(f"{Fore.YELLOW}⚠️  响应不是有效的JSON格式{Style.RESET_ALL}")
                    print(f"响应内容: {response.text[:500]}...")
            else:
                print(f"{Fore.RED}❌ 请求失败，状态码: {response.status_code}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ 请求异常: {str(e)}{Style.RESET_ALL}")
        
        return None

def main():
    extractor = DownloadLinkExtractor()
    
    # 从日志中提取链接
    links = extractor.extract_from_logs()
    
    if links:
        # 验证链接
        extractor.verify_links()
        
        # 保存到文件
        extractor.save_links_to_file()
        
        print(f"\n{Fore.GREEN}🎉 提取完成！{Style.RESET_ALL}")
        print(f"📊 总共找到 {len(links)} 个下载链接")
        
        # 显示最新的一个链接
        if links:
            latest_link = links[-1]
            print(f"\n{Fore.BLUE}🔗 最新的下载链接：{Style.RESET_ALL}")
            print(f"⏰ 时间: {latest_link['timestamp']}")
            url = latest_link['download_url']
            if len(url) > 150:
                print(f"📥 链接: {url[:75]}...{url[-75:]}")
            else:
                print(f"📥 链接: {url}")
    else:
        print(f"{Fore.YELLOW}⚠️  未找到任何下载链接{Style.RESET_ALL}")
        print("请确保：")
        print("1. 已运行代理服务器并抓取了API请求")
        print("2. 在APK中执行了下载操作")
        print("3. logs目录中存在API请求日志文件")

if __name__ == "__main__":
    main() 