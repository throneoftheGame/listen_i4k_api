#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载链接测试工具
测试提取的下载链接是否有效，或重新获取新的下载链接
"""

import requests
import json
from colorama import init, Fore, Style
import urllib.parse

# 初始化colorama
init()

def test_download_link(url):
    """测试下载链接是否有效"""
    print(f"{Fore.BLUE}🔍 测试下载链接{Style.RESET_ALL}")
    print(f"🔗 链接: {url[:100]}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        # 发送HEAD请求检查
        response = requests.head(url, headers=headers, timeout=15, allow_redirects=True)
        
        print(f"📊 状态码: {response.status_code}")
        print(f"📍 最终URL: {response.url}")
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ 链接有效！可以下载{Style.RESET_ALL}")
            
            # 显示文件信息
            if 'Content-Length' in response.headers:
                size = int(response.headers['Content-Length'])
                size_mb = size / (1024 * 1024)
                size_gb = size_mb / 1024
                if size_gb > 1:
                    print(f"📏 文件大小: {size_gb:.2f} GB")
                else:
                    print(f"📏 文件大小: {size_mb:.2f} MB")
            
            if 'Content-Type' in response.headers:
                print(f"📄 文件类型: {response.headers['Content-Type']}")
            
            # 提取文件名
            filename = extract_filename_from_url(url)
            if filename:
                print(f"📁 文件名: {filename}")
            
            return True
            
        elif response.status_code == 403:
            print(f"{Fore.YELLOW}⚠️  链接已过期或无权限访问{Style.RESET_ALL}")
            return False
        elif response.status_code == 404:
            print(f"{Fore.RED}❌ 文件不存在{Style.RESET_ALL}")
            return False
        else:
            print(f"{Fore.YELLOW}⚠️  其他状态: {response.status_code}{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ 测试失败: {str(e)}{Style.RESET_ALL}")
        return False

def extract_filename_from_url(url):
    """从URL中提取文件名"""
    try:
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # 从response-content-disposition参数中提取
        if 'response-content-disposition' in query_params:
            disposition = query_params['response-content-disposition'][0]
            disposition = urllib.parse.unquote(disposition)
            
            # 查找filename
            if 'filename*=UTF-8' in disposition:
                parts = disposition.split('filename*=UTF-8\'\'')
                if len(parts) > 1:
                    filename = parts[1].split(';')[0]
                    return urllib.parse.unquote(filename)
            elif 'filename=' in disposition:
                parts = disposition.split('filename=')
                if len(parts) > 1:
                    filename = parts[1].split(';')[0].strip('"\'')
                    return urllib.parse.unquote(filename)
        
        return None
    except:
        return None

def get_new_download_link():
    """尝试获取新的下载链接"""
    print(f"\n{Fore.BLUE}🚀 尝试获取新的下载链接{Style.RESET_ALL}")
    
    # 从提取的链接信息中获取参数
    try:
        with open('extracted_download_links.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data['links']:
            link_info = data['links'][0]  # 使用第一个链接的参数
            query_params = link_info['query_params']
            
            # 构建新的API请求
            api_url = "http://43.143.112.172:8168/aliyun/api.php"
            
            print(f"🔗 API请求: {api_url}")
            print(f"📋 参数: {json.dumps(query_params, ensure_ascii=False, indent=2)}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*'
            }
            
            response = requests.get(api_url, params=query_params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if 'url' in result:
                        new_url = result['url']
                        print(f"{Fore.GREEN}✅ 获取到新的下载链接！{Style.RESET_ALL}")
                        print(f"🔗 新链接: {new_url[:100]}...")
                        
                        # 测试新链接
                        if test_download_link(new_url):
                            # 保存新链接
                            save_new_link(new_url, query_params)
                        
                        return new_url
                    else:
                        print(f"{Fore.YELLOW}⚠️  响应中没有找到下载链接{Style.RESET_ALL}")
                        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                except:
                    print(f"{Fore.YELLOW}⚠️  响应不是有效JSON{Style.RESET_ALL}")
                    print(f"响应内容: {response.text[:500]}...")
            else:
                print(f"{Fore.RED}❌ API请求失败，状态码: {response.status_code}{Style.RESET_ALL}")
                
    except Exception as e:
        print(f"{Fore.RED}❌ 获取新链接失败: {str(e)}{Style.RESET_ALL}")
    
    return None

def save_new_link(url, params):
    """保存新的下载链接"""
    try:
        new_link_data = {
            "timestamp": "2025-05-28T17:40:00.000000",
            "download_url": url,
            "query_params": params,
            "status": "新获取"
        }
        
        with open('new_download_link.json', 'w', encoding='utf-8') as f:
            json.dump(new_link_data, f, ensure_ascii=False, indent=2)
        
        print(f"{Fore.GREEN}💾 新链接已保存到: new_download_link.json{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ 保存失败: {str(e)}{Style.RESET_ALL}")

def main():
    print(f"{Fore.GREEN}🎯 下载链接测试工具{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    # 读取提取的下载链接
    try:
        with open('extracted_download_links.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data['links']:
            original_url = data['links'][0]['download_url']
            
            print(f"\n📄 测试原始下载链接")
            is_valid = test_download_link(original_url)
            
            if not is_valid:
                print(f"\n🔄 原始链接无效，尝试获取新的下载链接...")
                new_url = get_new_download_link()
                
                if new_url:
                    print(f"\n{Fore.GREEN}🎉 成功！新的下载链接已准备就绪{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}😞 无法获取新的下载链接{Style.RESET_ALL}")
                    print("可能的原因：")
                    print("1. API服务器状态变化")
                    print("2. 认证参数已过期") 
                    print("3. 文件已被删除或移动")
                    print("\n建议：重新在APK中操作，抓取新的API请求")
            else:
                print(f"\n{Fore.GREEN}🎉 太好了！原始链接仍然有效，可以直接使用{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  没有找到已提取的下载链接{Style.RESET_ALL}")
            
    except FileNotFoundError:
        print(f"{Fore.RED}❌ 未找到 extracted_download_links.json 文件{Style.RESET_ALL}")
        print("请先运行 download_link_extractor.py 提取下载链接")
    except Exception as e:
        print(f"{Fore.RED}❌ 读取文件失败: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 