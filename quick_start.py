#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键启动HTTPS API抓取工具
"""

import subprocess
import sys
import os
import time
from colorama import init, Fore, Style

init()

def print_banner():
    """打印欢迎横幅"""
    print(f"{Fore.CYAN}")
    print("=" * 60)
    print("   🚀 Android HTTPS API抓取工具 - 一键启动")
    print("=" * 60)
    print(f"{Style.RESET_ALL}")

def check_adb():
    """检查ADB是否可用"""
    try:
        result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Fore.GREEN}✅ ADB已就绪{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ ADB不可用{Style.RESET_ALL}")
            return False
    except FileNotFoundError:
        print(f"{Fore.RED}❌ ADB未安装，请安装Android SDK{Style.RESET_ALL}")
        return False

def check_emulator():
    """检查模拟器状态"""
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = [line for line in result.stdout.split('\n') if 'emulator' in line and 'device' in line]
        if devices:
            print(f"{Fore.GREEN}✅ 检测到 {len(devices)} 个运行中的模拟器{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  未检测到运行中的模拟器{Style.RESET_ALL}")
            return False
    except:
        return False

def main():
    """主函数"""
    print_banner()
    
    print(f"{Fore.BLUE}🔍 正在检查系统环境...{Style.RESET_ALL}")
    
    # 检查ADB
    adb_ok = check_adb()
    
    # 检查模拟器
    emulator_ok = check_emulator()
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📋 操作指南{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if not adb_ok:
        print(f"{Fore.RED}❌ 请先安装Android SDK并将adb添加到PATH{Style.RESET_ALL}")
        return
    
    if not emulator_ok:
        print(f"{Fore.YELLOW}💡 请先启动Android模拟器，然后重新运行此脚本{Style.RESET_ALL}")
        answer = input(f"{Fore.CYAN}是否继续配置流程？(y/n): {Style.RESET_ALL}").strip().lower()
        if answer != 'y':
            return
    
    print(f"\n{Fore.YELLOW}请按照以下步骤操作:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. 配置模拟器代理设置{Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. 启动代理服务器{Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. 安装HTTPS证书{Style.RESET_ALL}")
    print(f"{Fore.WHITE}4. 开始抓取API{Style.RESET_ALL}")
    
    while True:
        print(f"\n{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}选择操作:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. 配置模拟器代理设置{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. 启动代理服务器{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. 查看证书安装指南{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. 分析抓取的日志{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}5. 重置代理设置{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}0. 退出{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}请选择 (0-5): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            print(f"\n{Fore.BLUE}🔧 配置模拟器代理设置...{Style.RESET_ALL}")
            subprocess.run([sys.executable, "setup_android_proxy.py"])
            
        elif choice == "2":
            print(f"\n{Fore.BLUE}🚀 启动代理服务器...{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}💡 提示: 代理服务器启动后，请在另一个终端窗口操作模拟器{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}💡 提示: 按 Ctrl+C 可停止代理服务器{Style.RESET_ALL}")
            input(f"{Fore.CYAN}按Enter键继续...{Style.RESET_ALL}")
            subprocess.run([sys.executable, "start_proxy.py"])
            
        elif choice == "3":
            print(f"\n{Fore.BLUE}📜 查看证书安装指南...{Style.RESET_ALL}")
            subprocess.run([sys.executable, "setup_android_proxy.py", "cert"])
            
        elif choice == "4":
            print(f"\n{Fore.BLUE}📊 启动日志分析工具...{Style.RESET_ALL}")
            subprocess.run([sys.executable, "log_analyzer.py"])
            
        elif choice == "5":
            print(f"\n{Fore.BLUE}🔄 重置代理设置...{Style.RESET_ALL}")
            subprocess.run([sys.executable, "setup_android_proxy.py", "reset"])
            
        elif choice == "0":
            print(f"\n{Fore.GREEN}👋 感谢使用！{Style.RESET_ALL}")
            break
            
        else:
            print(f"{Fore.RED}❌ 无效选择，请重新输入{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 