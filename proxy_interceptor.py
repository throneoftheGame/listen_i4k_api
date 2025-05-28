#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTPS接口抓取器
用于抓取Android模拟器中APK的接口请求信息
"""

import json
import time
import os
from datetime import datetime
from mitmproxy import http, ctx
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
from colorama import init, Fore, Style
import threading
import signal
import sys

# 初始化colorama
init()

class HTTPSInterceptor:
    def __init__(self):
        self.requests_log = []
        self.log_file = f"api_requests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.console_log_file = f"console_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # 创建日志目录
        os.makedirs("logs", exist_ok=True)
        self.log_file = os.path.join("logs", self.log_file)
        self.console_log_file = os.path.join("logs", self.console_log_file)
        
        print(f"{Fore.GREEN}🚀 HTTP/HTTPS接口抓取器已启动{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📝 日志文件: {self.log_file}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 控制台日志: {self.console_log_file}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    def request(self, flow: http.HTTPFlow):
        """处理HTTP请求"""
        request = flow.request
        
        # 记录所有HTTP和HTTPS请求
        request_info = {
            "timestamp": datetime.now().isoformat(),
            "method": request.method,
            "url": request.pretty_url,
            "scheme": request.scheme,  # 添加协议类型
            "host": request.host,
            "path": request.path,
            "headers": dict(request.headers),
            "query_params": dict(request.query) if request.query else {},
            "body": None,
            "body_size": len(request.content) if request.content else 0
        }
        
        # 处理请求体
        if request.content:
            try:
                # 尝试解析JSON
                if 'application/json' in request.headers.get('content-type', ''):
                    request_info["body"] = json.loads(request.content.decode('utf-8'))
                # 尝试解析表单数据
                elif 'application/x-www-form-urlencoded' in request.headers.get('content-type', ''):
                    from urllib.parse import parse_qs
                    request_info["body"] = dict(parse_qs(request.content.decode('utf-8')))
                else:
                    # 其他格式保存为字符串（如果是文本）
                    try:
                        request_info["body"] = request.content.decode('utf-8')
                    except:
                        request_info["body"] = f"<二进制数据: {len(request.content)} 字节>"
            except Exception as e:
                request_info["body"] = f"<解析失败: {str(e)}>"
        
        # 保存到内存
        setattr(flow, 'request_info', request_info)
        
        # 实时显示请求信息
        self._print_request(request_info)

    def response(self, flow: http.HTTPFlow):
        """处理HTTP响应"""
        if hasattr(flow, 'request_info'):
            response = flow.response
            request_info = getattr(flow, 'request_info')
            
            response_info = {
                "status_code": response.status_code,
                "status_text": response.reason,
                "headers": dict(response.headers),
                "body": None,
                "body_size": len(response.content) if response.content else 0,
                "response_time": None  # mitmproxy不直接提供响应时间
            }
            
            # 处理响应体 - 显示完整内容
            if response.content:
                try:
                    # 尝试解析JSON
                    if 'application/json' in response.headers.get('content-type', ''):
                        response_info["body"] = json.loads(response.content.decode('utf-8'))
                    # HTML内容 - 显示完整内容
                    elif 'text/html' in response.headers.get('content-type', ''):
                        response_info["body"] = response.content.decode('utf-8')
                    # 纯文本 - 显示完整内容
                    elif 'text/plain' in response.headers.get('content-type', ''):
                        response_info["body"] = response.content.decode('utf-8')
                    else:
                        # 其他格式 - 尝试显示完整文本内容
                        try:
                            response_info["body"] = response.content.decode('utf-8')
                        except:
                            response_info["body"] = f"<二进制数据: {len(response.content)} 字节>"
                except Exception as e:
                    response_info["body"] = f"<解析失败: {str(e)}>"
            
            # 合并请求和响应信息
            complete_info = {
                "request": request_info,
                "response": response_info
            }
            
            # 添加到日志列表
            self.requests_log.append(complete_info)
            
            # 实时显示响应信息
            self._print_response(response_info)
            
            # 保存到文件
            self._save_to_file(complete_info)

    def _print_request(self, request_info):
        """打印请求信息到控制台"""
        scheme_color = Fore.GREEN if request_info['scheme'] == 'https' else Fore.BLUE
        print(f"\n{scheme_color}📤 [{request_info['scheme'].upper()}请求] {request_info['method']} {request_info['url']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⏰ 时间: {request_info['timestamp']}{Style.RESET_ALL}")
        
        if request_info['query_params']:
            print(f"{Fore.CYAN}🔍 查询参数: {json.dumps(request_info['query_params'], ensure_ascii=False, indent=2)}{Style.RESET_ALL}")
        
        if request_info['body']:
            print(f"{Fore.MAGENTA}📦 请求体: {json.dumps(request_info['body'], ensure_ascii=False, indent=2) if isinstance(request_info['body'], (dict, list)) else request_info['body']}{Style.RESET_ALL}")
        
        # 同时写入控制台日志文件
        with open(self.console_log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{request_info['scheme'].upper()}请求] {request_info['method']} {request_info['url']}\n")
            f.write(f"时间: {request_info['timestamp']}\n")
            if request_info['query_params']:
                f.write(f"查询参数: {json.dumps(request_info['query_params'], ensure_ascii=False, indent=2)}\n")
            if request_info['body']:
                f.write(f"请求体: {json.dumps(request_info['body'], ensure_ascii=False, indent=2) if isinstance(request_info['body'], (dict, list)) else request_info['body']}\n")

    def _print_response(self, response_info):
        """打印响应信息到控制台"""
        status_color = Fore.GREEN if 200 <= response_info['status_code'] < 300 else Fore.RED
        print(f"{status_color}📥 [响应] {response_info['status_code']} {response_info['status_text']}{Style.RESET_ALL}")
        
        if response_info['body']:
            # 显示完整的响应体内容
            if isinstance(response_info['body'], (dict, list)):
                body_display = json.dumps(response_info['body'], ensure_ascii=False, indent=2)
            else:
                body_display = str(response_info['body'])
            
            print(f"{Fore.GREEN}📄 响应体完整内容: {body_display}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # 同时写入控制台日志文件
        with open(self.console_log_file, 'a', encoding='utf-8') as f:
            f.write(f"[响应] {response_info['status_code']} {response_info['status_text']}\n")
            if response_info['body']:
                if isinstance(response_info['body'], (dict, list)):
                    body_display = json.dumps(response_info['body'], ensure_ascii=False, indent=2)
                else:
                    body_display = str(response_info['body'])
                f.write(f"响应体: {body_display}\n")
            f.write("="*60 + "\n")

    def _save_to_file(self, complete_info):
        """保存完整的请求响应信息到JSON文件"""
        try:
            # 读取现有数据
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            
            # 添加新数据
            data.append(complete_info)
            
            # 写回文件
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"{Fore.RED}❌ 保存文件失败: {str(e)}{Style.RESET_ALL}")

# 创建拦截器实例
interceptor = HTTPSInterceptor()

# mitmproxy插件函数
def request(flow: http.HTTPFlow):
    interceptor.request(flow)

def response(flow: http.HTTPFlow):
    interceptor.response(flow)

if __name__ == "__main__":
    print("请使用 'python start_proxy.py' 来启动代理服务器") 