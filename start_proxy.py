#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动HTTPS代理服务器
"""

import subprocess
import sys
import os
import signal
from colorama import init, Fore, Style

init()

def start_proxy():
    """启动mitmproxy代理服务器"""
    print(f"{Fore.GREEN}🚀 启动HTTPS接口抓取代理服务器...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📡 代理地址: 127.0.0.1:8080{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}💡 请在Android模拟器中设置代理为: 10.0.2.2:8080{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}💡 并安装mitmproxy证书来抓取HTTPS流量{Style.RESET_ALL}")
    print(f"{Fore.RED}⚠️  按 Ctrl+C 停止代理服务器{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    try:
        # 使用最简单的mitmdump启动方式
        cmd = [
            "mitmdump",
            "-s", "proxy_interceptor.py",
            "-p", "8080"
        ]
        
        print(f"{Fore.BLUE}📋 执行命令: {' '.join(cmd)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}🎯 代理服务器启动中...{Style.RESET_ALL}\n")
        
        # 启动代理服务器
        process = subprocess.run(cmd, check=True)
        
    except FileNotFoundError:
        print(f"{Fore.RED}❌ 找不到mitmdump命令{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 请确保已安装mitmproxy: pip install -r requirements.txt{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 正在停止代理服务器...{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ 代理服务器已停止{Style.RESET_ALL}")
        
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}❌ 启动代理服务器失败: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 请确保端口8080未被占用{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 或者尝试手动运行: mitmdump -s proxy_interceptor.py -p 8080{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ 未知错误: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    start_proxy() 