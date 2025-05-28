#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云盘URL分析器
用于分析阿里云盘下载链接的生成机制和组成部分
"""

import base64
import json
import urllib.parse
from datetime import datetime, timezone
from colorama import init, Fore, Style

# 初始化colorama
init()

class AliyunDriveURLAnalyzer:
    def __init__(self):
        self.analysis_result = {}
    
    def analyze_url(self, url):
        """分析阿里云盘URL"""
        print(f"{Fore.GREEN}🔍 开始分析阿里云盘下载链接{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        # 解析URL
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # 基本信息
        self._analyze_basic_info(parsed_url)
        
        # 分析路径
        self._analyze_path(parsed_url.path)
        
        # 分析查询参数
        self._analyze_query_params(query_params)
        
        # 分析生成机制
        self._analyze_generation_mechanism()
        
        return self.analysis_result
    
    def _analyze_basic_info(self, parsed_url):
        """分析基本信息"""
        print(f"\n{Fore.YELLOW}📍 基本信息分析{Style.RESET_ALL}")
        print(f"🌐 域名: {parsed_url.hostname}")
        print(f"🔗 协议: {parsed_url.scheme}")
        print(f"📂 路径: {parsed_url.path}")
        
        # 域名分析
        if 'aliyundrive.net' in parsed_url.hostname:
            region = parsed_url.hostname.split('.')[0].replace('cn-', '').replace('-data', '')
            print(f"🌍 数据中心: {region} (北京)")
            print(f"☁️  服务类型: 阿里云盘数据存储服务")
    
    def _analyze_path(self, path):
        """分析路径结构"""
        print(f"\n{Fore.YELLOW}📁 路径结构分析{Style.RESET_ALL}")
        
        # URL解码路径
        decoded_path = urllib.parse.unquote(path)
        path_parts = decoded_path.strip('/').split('/')
        
        print(f"🔢 路径层级数: {len(path_parts)}")
        for i, part in enumerate(path_parts):
            if i == 0:
                print(f"   层级 {i+1}: {part} (存储桶标识)")
            elif i == 1:
                print(f"   层级 {i+1}: {part} (用户/项目ID)")
            else:
                print(f"   层级 {i+1}: {part} (文件哈希/路径)")
    
    def _analyze_query_params(self, query_params):
        """分析查询参数"""
        print(f"\n{Fore.YELLOW}🔧 查询参数分析{Style.RESET_ALL}")
        
        for key, values in query_params.items():
            value = values[0] if values else ""
            
            if key == 'callback':
                print(f"📞 {key}: 回调配置")
                self._decode_base64_param("回调信息", value)
                
            elif key == 'callback-var':
                print(f"📋 {key}: 回调变量")
                self._decode_base64_param("回调变量", value)
                
            elif key == 'security-token':
                print(f"🔐 {key}: 安全令牌 (STS临时凭证)")
                print(f"   长度: {len(value)} 字符")
                
            elif key == 'x-oss-access-key-id':
                print(f"🔑 {key}: OSS访问密钥ID")
                print(f"   值: {value}")
                
            elif key == 'x-oss-expires':
                print(f"⏰ {key}: 链接过期时间")
                try:
                    expire_time = datetime.fromtimestamp(int(value), tz=timezone.utc)
                    print(f"   过期时间: {expire_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                except:
                    print(f"   原始值: {value}")
                    
            elif key == 'x-oss-signature':
                print(f"✍️  {key}: OSS签名")
                print(f"   签名值: {value}")
                
            elif key == 'response-content-disposition':
                print(f"📥 {key}: 下载配置")
                decoded_value = urllib.parse.unquote(value)
                print(f"   配置: {decoded_value}")
                
            elif key == 'pds-params':
                print(f"⚙️  {key}: 应用参数")
                try:
                    decoded_json = urllib.parse.unquote(value)
                    params = json.loads(decoded_json)
                    print(f"   参数: {json.dumps(params, ensure_ascii=False, indent=6)}")
                except:
                    print(f"   原始值: {value}")
                    
            else:
                print(f"🏷️  {key}: {value}")
    
    def _decode_base64_param(self, param_name, encoded_value):
        """解码base64参数"""
        try:
            # URL解码
            url_decoded = urllib.parse.unquote(encoded_value)
            # Base64解码
            decoded_bytes = base64.b64decode(url_decoded + '==')  # 添加填充
            decoded_str = decoded_bytes.decode('utf-8')
            
            # 尝试解析为JSON
            try:
                json_data = json.loads(decoded_str)
                print(f"   {param_name}内容:")
                print(f"   {json.dumps(json_data, ensure_ascii=False, indent=6)}")
            except:
                print(f"   {param_name}内容: {decoded_str}")
                
        except Exception as e:
            print(f"   解码失败: {str(e)}")
    
    def _analyze_generation_mechanism(self):
        """分析生成机制"""
        print(f"\n{Fore.GREEN}🛠️  URL生成机制分析{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        print("📋 生成步骤:")
        print("   1. 用户请求文件下载")
        print("   2. 服务器验证用户权限")
        print("   3. 生成STS临时凭证")
        print("   4. 构建OSS预签名URL")
        print("   5. 添加回调和下载配置")
        print("   6. 返回完整下载链接")
        
        print(f"\n🔐 安全机制:")
        print("   • STS临时令牌 (有时效性)")
        print("   • OSS签名验证 (防篡改)")
        print("   • 域名限制 (防盗链)")
        print("   • 过期时间控制")
        
        print(f"\n🏗️  技术架构:")
        print("   • 阿里云OSS对象存储")
        print("   • STS临时授权服务") 
        print("   • 预签名URL机制")
        print("   • 回调机制确保安全")
        
        print(f"\n⚡ 生成算法:")
        print("   1. 使用AccessKey和SecretKey")
        print("   2. 结合请求参数生成签名")
        print("   3. 设置过期时间戳")
        print("   4. URL编码所有参数")
        print("   5. 组装最终下载链接")

def main():
    # 示例URL
    sample_url = """https://cn-beijing-data.aliyundrive.net/kB869cMH%2F889036%2F682feb616199780d9a4c472b85300752445328b4%2F682feb61aee4515451ce4576bd8da990cfc049d2?callback=eyJjYWxsYmFja1VybCI6Imh0dHA6Ly9iajI5LmFwaS1ocC5hbGl5dW5wZHMuY29tL3YyL2ZpbGUvZG93bmxvYWRfY2FsbGJhY2siLCJjYWxsYmFja0JvZHkiOiJodHRwSGVhZGVyLnJhbmdlPSR7aHR0cEhlYWRlci5yYW5nZX1cdTAwMjZidWNrZXQ9JHtidWNrZXR9XHUwMDI2b2JqZWN0PSR7b2JqZWN0fVx1MDAyNmRvbWFpbl9pZD0ke3g6ZG9tYWluX2lkfVx1MDAyNnVzZXJfaWQ9JHt4OnVzZXJfaWR9XHUwMDI2ZHJpdmVfaWQ9JHt4OmRyaXZlX2lkfVx1MDAyNmZpbGVfaWQ9JHt4OmZpbGVfaWR9XHUwMDI2cGRzX3BhcmFtcz0ke3g6cGRzX3BhcmFtc31cdTAwMjZ2ZXJzaW9uPSR7eDp2ZXJzaW9ufSIsImNhbGxiYWNrQm9keVR5cGUiOiJhcHBsaWNhdGlvbi94LXd3dy1mb3JtLXVybGVuY29kZWQiLCJjYWxsYmFja1N0YWdlIjoiYmVmb3JlLWV4ZWN1dGUiLCJjYWxsYmFja0ZhaWx1cmVBY3Rpb24iOiJpZ25vcmUifQ%3D%3D&callback-var=eyJ4OmRvbWFpbl9pZCI6ImJqMjkiLCJ4OnVzZXJfaWQiOiJkZTc2ZDE4ODQzM2U0MThjOWY3NWJkNDk4YWE3YWRjNiIsIng6ZHJpdmVfaWQiOiI3ODI1NTY2IiwieDpmaWxlX2lkIjoiNjgzNmQwYzcyMWQ2ZDgxNjhhMTY0OGVhOGYyMDQwYzExZDQ4NmZhMSIsIng6cGRzX3BhcmFtcyI6IntcImFwXCI6XCJwSlpJbk5ITjJkWldrOHFnXCJ9IiwieDp2ZXJzaW9uIjoidjMifQ%3D%3D&di=bj29&dr=7825566&f=6836d0c721d6d8168a1648ea8f2040c11d486fa1&pds-params=%7B%22ap%22%3A%22pJZInNHN2dZWk8qg%22%7D&response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%27S02E01.2025.2160p.WEB-DL.H265.AAC%25281%2529.mp4&security-token=CAISvgJ1q6Ft5B2yfSjIr5XFD8CAo5pQ5o%2B5WGzeh1QQeNpNp6%2F%2BmDz2IHhMf3NpBOkZvvQ1lGlU6%2Fcalq5rR4QAXlDfNWrEBRbOq1HPWZHInuDox55m4cTXNAr%2BIhr%2F29CoEIedZdjBe%2FCrRknZnytou9XTfimjWFrXWv%2Fgy%2BQQDLItUxK%2FcCBNCfpPOwJms7V6D3bKMuu3OROY6Qi5TmgQ41Uh1jgjtPzkkpfFtkGF1GeXkLFF%2B97DRbG%2FdNRpMZtFVNO44fd7bKKp0lQLs0ARrv4r1fMUqW2X543AUgFLhy2KKMPY99xpFgh9a7j0iCbSGyUu%2FhcRm5sw9%2Byfo34lVYneAzXVwnJH7uHwufJ7FxfIREfquk63pvSlHLcLPe0Kjzzleo2k1XRPVFF%2B535IaHXuToXDnvSiTe68X%2FXtuMkagAFtMyfEwDUgiut8BnIL0WImMmhKb02oKIgf3Asw4krtiWS7LjqF7Ot7dq3QaPYLvBjem4WZOsJa3nuGfq07cxjI9RB%2B4XVEakQNxRyYI0ainuwA4LJao2bxEGwZ%2B0gG94GNFTjaSelsMTJ%2F0zNYMFsHHUUkv4iY%2FDf92Q6wDByfeyAA&u=de76d188433e418c9f75bd498aa7adc6&x-oss-access-key-id=STS.NVpDz4NEqQMRZJocTEtUaHjUz&x-oss-expires=1748538055&x-oss-signature=Usb%2Fe%2BB4EyD%2BypwobRI%2FPrRkstbltt2ZZ5A%2FQcU3MqQ%3D&x-oss-signature-version=OSS2"""
    
    analyzer = AliyunDriveURLAnalyzer()
    analyzer.analyze_url(sample_url)

if __name__ == "__main__":
    main() 