#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键启动下载链接捕获工具
整合所有功能，提供简单易用的操作界面
"""

import os
import sys
import time
import json
import subprocess
import threading
from datetime import datetime
from colorama import init, Fore, Style

# 初始化colorama
init()

class DownloadCaptureManager:
    def __init__(self):
        self.proxy_process = None
        self.is_capturing = False
        
    def show_welcome(self):
        """显示欢迎界面"""
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}🎯 阿里云盘下载链接捕获工具{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}功能介绍：{Style.RESET_ALL}")
        print("📱 抓取APK应用的下载请求")
        print("🔗 自动提取真实下载链接")
        print("✅ 验证链接有效性")
        print("💾 保存结果到文件")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    
    def check_environment(self):
        """检查运行环境"""
        print(f"\n{Fore.BLUE}🔍 检查运行环境{Style.RESET_ALL}")
        
        # 检查必要的文件
        required_files = [
            'proxy_interceptor.py',
            'download_link_extractor.py',
            'start_proxy.py'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"{Fore.RED}❌ 缺少必要文件: {', '.join(missing_files)}{Style.RESET_ALL}")
            return False
        
        # 检查logs目录
        if not os.path.exists('logs'):
            os.makedirs('logs')
            print(f"{Fore.GREEN}✅ 创建logs目录{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ 环境检查通过{Style.RESET_ALL}")
        return True
    
    def show_menu(self):
        """显示操作菜单"""
        print(f"\n{Fore.YELLOW}📋 请选择操作：{Style.RESET_ALL}")
        print("1. 🚀 启动代理并开始捕获 (新手推荐)")
        print("2. 📊 分析现有日志中的下载链接")
        print("3. 🔍 查看代理状态")
        print("4. 📁 查看所有日志文件")
        print("5. 🛠️  测试已提取的下载链接")
        print("6. ❌ 退出")
        print(f"{Fore.CYAN}{'-'*40}{Style.RESET_ALL}")
    
    def start_proxy_capture(self):
        """启动代理并开始捕获"""
        print(f"\n{Fore.GREEN}🚀 启动代理服务器{Style.RESET_ALL}")
        
        try:
            # 启动代理服务器
            self.proxy_process = subprocess.Popen([
                'mitmdump', '-s', 'proxy_interceptor.py', '-p', '8080'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print(f"{Fore.GREEN}✅ 代理服务器已启动 (端口: 8080){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}📱 现在请配置你的Android模拟器：{Style.RESET_ALL}")
            print("   1. 设置代理: 10.0.2.2:8080")
            print("   2. 安装证书: 访问 mitm.it 下载证书")
            print("   3. 在APK中点击下载按钮")
            print(f"{Fore.CYAN}🔄 正在实时监听网络请求...{Style.RESET_ALL}")
            
            self.is_capturing = True
            self.monitor_capture()
            
        except FileNotFoundError:
            print(f"{Fore.RED}❌ 找不到mitmdump命令{Style.RESET_ALL}")
            print("请确保已安装mitmproxy: pip install mitmproxy")
        except Exception as e:
            print(f"{Fore.RED}❌ 启动失败: {str(e)}{Style.RESET_ALL}")
    
    def monitor_capture(self):
        """监控捕获过程"""
        print(f"\n{Fore.BLUE}📡 监控模式已启动{Style.RESET_ALL}")
        print("💡 提示：")
        print("   - 每当APK发送下载请求时，会自动显示在终端")
        print("   - 按 Ctrl+C 停止捕获并分析结果")
        print("   - 请在APK中执行下载操作...")
        
        try:
            # 等待用户操作
            while self.is_capturing:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏹️  捕获已停止{Style.RESET_ALL}")
            self.stop_proxy()
            self.analyze_captured_data()
    
    def stop_proxy(self):
        """停止代理服务器"""
        if self.proxy_process:
            self.proxy_process.terminate()
            print(f"{Fore.GREEN}✅ 代理服务器已停止{Style.RESET_ALL}")
            self.is_capturing = False
    
    def analyze_captured_data(self):
        """分析捕获的数据"""
        print(f"\n{Fore.BLUE}📊 分析捕获的数据{Style.RESET_ALL}")
        
        # 运行下载链接提取器
        try:
            result = subprocess.run([
                'python', 'download_link_extractor.py'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"{Fore.GREEN}✅ 数据分析完成{Style.RESET_ALL}")
                self.show_results()
            else:
                print(f"{Fore.RED}❌ 分析失败: {result.stderr}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ 分析异常: {str(e)}{Style.RESET_ALL}")
    
    def show_results(self):
        """显示分析结果"""
        try:
            if os.path.exists('extracted_download_links.json'):
                with open('extracted_download_links.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"\n{Fore.GREEN}🎉 发现下载链接！{Style.RESET_ALL}")
                print(f"📊 总数量: {data['total_links']}")
                print(f"⏰ 提取时间: {data['extracted_time']}")
                
                if data['links']:
                    latest = data['links'][-1]
                    print(f"\n{Fore.BLUE}📥 最新下载链接：{Style.RESET_ALL}")
                    print(f"🔗 请求: {latest['request_url'][:80]}...")
                    print(f"📁 文件: 从URL参数可以看出文件类型")
                    
                    # 提取文件名
                    url = latest['download_url']
                    if 'filename' in url:
                        import urllib.parse
                        parsed = urllib.parse.urlparse(url)
                        params = urllib.parse.parse_qs(parsed.query)
                        if 'response-content-disposition' in params:
                            disposition = urllib.parse.unquote(params['response-content-disposition'][0])
                            print(f"📄 文件名: {disposition}")
                
                print(f"\n{Fore.YELLOW}💡 下一步操作：{Style.RESET_ALL}")
                print("1. 选择菜单选项5测试链接有效性")
                print("2. 如果链接过期，重新在APK中操作")
                print("3. 使用下载工具下载文件")
            else:
                print(f"{Fore.YELLOW}⚠️  未发现下载链接{Style.RESET_ALL}")
                print("请确保在APK中执行了下载操作")
                
        except Exception as e:
            print(f"{Fore.RED}❌ 显示结果失败: {str(e)}{Style.RESET_ALL}")
    
    def analyze_existing_logs(self):
        """分析现有日志"""
        print(f"\n{Fore.BLUE}📊 分析现有日志文件{Style.RESET_ALL}")
        os.system('python download_link_extractor.py')
    
    def check_proxy_status(self):
        """检查代理状态"""
        print(f"\n{Fore.BLUE}🔍 检查代理状态{Style.RESET_ALL}")
        
        if self.is_capturing:
            print(f"{Fore.GREEN}✅ 代理服务器正在运行 (PID: {self.proxy_process.pid}){Style.RESET_ALL}")
            print(f"📱 模拟器代理配置: 10.0.2.2:8080")
        else:
            print(f"{Fore.YELLOW}⚠️  代理服务器未运行{Style.RESET_ALL}")
            
        # 检查日志文件
        if os.path.exists('logs'):
            log_files = [f for f in os.listdir('logs') if f.endswith('.json')]
            print(f"📁 日志文件数量: {len(log_files)}")
    
    def list_log_files(self):
        """列出所有日志文件"""
        print(f"\n{Fore.BLUE}📁 日志文件列表{Style.RESET_ALL}")
        
        if os.path.exists('logs'):
            files = os.listdir('logs')
            json_files = [f for f in files if f.endswith('.json')]
            txt_files = [f for f in files if f.endswith('.txt')]
            
            print(f"📊 JSON日志文件 ({len(json_files)}个):")
            for f in json_files:
                file_path = os.path.join('logs', f)
                size = os.path.getsize(file_path)
                print(f"   {f} ({size} bytes)")
            
            print(f"\n📝 控制台日志文件 ({len(txt_files)}个):")
            for f in txt_files:
                file_path = os.path.join('logs', f)
                size = os.path.getsize(file_path)
                print(f"   {f} ({size} bytes)")
        else:
            print(f"{Fore.YELLOW}⚠️  logs目录不存在{Style.RESET_ALL}")
    
    def test_extracted_links(self):
        """测试已提取的下载链接"""
        print(f"\n{Fore.BLUE}🔍 测试下载链接{Style.RESET_ALL}")
        os.system('python test_download_link.py')
    
    def run(self):
        """运行主程序"""
        self.show_welcome()
        
        if not self.check_environment():
            print(f"{Fore.RED}❌ 环境检查失败，程序退出{Style.RESET_ALL}")
            return
        
        while True:
            self.show_menu()
            
            try:
                choice = input(f"{Fore.YELLOW}请输入选项 (1-6): {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    self.start_proxy_capture()
                elif choice == '2':
                    self.analyze_existing_logs()
                elif choice == '3':
                    self.check_proxy_status()
                elif choice == '4':
                    self.list_log_files()
                elif choice == '5':
                    self.test_extracted_links()
                elif choice == '6':
                    if self.is_capturing:
                        self.stop_proxy()
                    print(f"{Fore.GREEN}👋 再见！{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}❌ 无效选项，请输入1-6{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                if self.is_capturing:
                    self.stop_proxy()
                print(f"\n{Fore.GREEN}👋 程序已退出{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ 操作失败: {str(e)}{Style.RESET_ALL}")

def main():
    manager = DownloadCaptureManager()
    manager.run()

if __name__ == "__main__":
    main() 