#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android模拟器代理配置脚本
"""

import subprocess
import sys
import os
from colorama import init, Fore, Style

init()

def setup_android_proxy():
    """配置Android模拟器代理设置"""
    print(f"{Fore.GREEN}🤖 Android模拟器代理配置工具{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    # 检查adb是否可用
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{Fore.RED}❌ ADB不可用，请确保Android SDK已安装并添加到PATH{Style.RESET_ALL}")
            return False
        
        devices = [line for line in result.stdout.split('\n') if 'emulator' in line and 'device' in line]
        if not devices:
            print(f"{Fore.RED}❌ 未检测到运行中的Android模拟器{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 请先启动Android模拟器{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.GREEN}✅ 检测到 {len(devices)} 个模拟器{Style.RESET_ALL}")
        
    except FileNotFoundError:
        print(f"{Fore.RED}❌ 未找到adb命令，请安装Android SDK{Style.RESET_ALL}")
        return False
    
    # 配置代理
    proxy_host = "10.0.2.2"  # 模拟器访问主机的特殊IP
    proxy_port = "8080"
    
    print(f"{Fore.YELLOW}📡 配置代理: {proxy_host}:{proxy_port}{Style.RESET_ALL}")
    
    try:
        # 启用代理
        subprocess.run(['adb', 'shell', 'settings', 'put', 'global', 'http_proxy', f'{proxy_host}:{proxy_port}'], check=True)
        print(f"{Fore.GREEN}✅ 已配置HTTP代理{Style.RESET_ALL}")
        
        # 配置HTTPS代理（某些版本的Android）
        subprocess.run(['adb', 'shell', 'settings', 'put', 'global', 'https_proxy', f'{proxy_host}:{proxy_port}'], check=True)
        print(f"{Fore.GREEN}✅ 已配置HTTPS代理{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}📋 下一步操作:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. 下载并安装mitmproxy证书到模拟器{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. 在模拟器浏览器中访问: mitm.it{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. 下载Android证书并安装{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. 启动代理服务器: python start_proxy.py{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}5. 在模拟器中使用您的APK{Style.RESET_ALL}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}❌ 配置代理失败: {e}{Style.RESET_ALL}")
        return False

def reset_android_proxy():
    """重置Android模拟器代理设置"""
    print(f"{Fore.YELLOW}🔄 重置模拟器代理设置...{Style.RESET_ALL}")
    
    try:
        subprocess.run(['adb', 'shell', 'settings', 'delete', 'global', 'http_proxy'], check=True)
        subprocess.run(['adb', 'shell', 'settings', 'delete', 'global', 'https_proxy'], check=True)
        print(f"{Fore.GREEN}✅ 已重置代理设置{Style.RESET_ALL}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}❌ 重置代理失败: {e}{Style.RESET_ALL}")
        return False

def install_certificate():
    """帮助安装mitmproxy证书"""
    print(f"{Fore.GREEN}📜 mitmproxy证书安装指南{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}步骤 1: 确保代理服务器正在运行{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}步骤 2: 在模拟器中打开浏览器{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}步骤 3: 访问 http://mitm.it{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}步骤 4: 点击 'Get mitmproxy-ca-cert.pem'{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}步骤 5: 在Android设置中安装证书{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   - 设置 > 安全 > 加密和凭据 > 从存储设备安装{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}步骤 6: 选择下载的证书文件并命名{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "reset":
            reset_android_proxy()
        elif sys.argv[1] == "cert":
            install_certificate()
        else:
            print(f"{Fore.YELLOW}用法: python setup_android_proxy.py [reset|cert]{Style.RESET_ALL}")
    else:
        setup_android_proxy() 