#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API请求日志分析工具
"""

import json
import os
import glob
from datetime import datetime
from collections import defaultdict
from colorama import init, Fore, Style

init()

class LogAnalyzer:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.data = []
        
    def load_logs(self, log_file=None):
        """加载日志文件"""
        if log_file:
            log_files = [log_file]
        else:
            # 自动找到最新的日志文件
            pattern = os.path.join(self.log_dir, "api_requests_*.json")
            log_files = glob.glob(pattern)
            
        if not log_files:
            print(f"{Fore.RED}❌ 未找到日志文件{Style.RESET_ALL}")
            return False
        
        # 如果有多个文件，使用最新的
        latest_file = max(log_files, key=os.path.getctime)
        print(f"{Fore.GREEN}📂 加载日志文件: {latest_file}{Style.RESET_ALL}")
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"{Fore.GREEN}✅ 成功加载 {len(self.data)} 条记录{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ 加载日志失败: {e}{Style.RESET_ALL}")
            return False
    
    def analyze_summary(self):
        """分析总览"""
        if not self.data:
            print(f"{Fore.RED}❌ 没有数据可分析{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 API请求分析总览{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # 基本统计
        total_requests = len(self.data)
        print(f"{Fore.YELLOW}📈 总请求数: {total_requests}{Style.RESET_ALL}")
        
        # 按域名分类
        domains = defaultdict(int)
        methods = defaultdict(int)
        status_codes = defaultdict(int)
        
        for record in self.data:
            request = record.get('request', {})
            response = record.get('response', {})
            
            domains[request.get('host', 'unknown')] += 1
            methods[request.get('method', 'unknown')] += 1
            status_codes[response.get('status_code', 'unknown')] += 1
        
        # 显示统计信息
        print(f"\n{Fore.BLUE}🌐 请求域名分布:{Style.RESET_ALL}")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
            print(f"  {domain}: {count}")
        
        print(f"\n{Fore.BLUE}📤 请求方法分布:{Style.RESET_ALL}")
        for method, count in sorted(methods.items(), key=lambda x: x[1], reverse=True):
            print(f"  {method}: {count}")
        
        print(f"\n{Fore.BLUE}📥 响应状态码分布:{Style.RESET_ALL}")
        for status, count in sorted(status_codes.items(), key=lambda x: x[1], reverse=True):
            color = Fore.GREEN if str(status).startswith('2') else Fore.RED if str(status).startswith('4') or str(status).startswith('5') else Fore.YELLOW
            print(f"  {color}{status}: {count}{Style.RESET_ALL}")
    
    def search_requests(self, keyword=None, method=None, status_code=None):
        """搜索特定请求"""
        if not self.data:
            print(f"{Fore.RED}❌ 没有数据可搜索{Style.RESET_ALL}")
            return
        
        filtered_data = self.data
        
        # 按关键词过滤
        if keyword:
            filtered_data = [
                record for record in filtered_data
                if keyword.lower() in record.get('request', {}).get('url', '').lower()
                or keyword.lower() in record.get('request', {}).get('host', '').lower()
            ]
        
        # 按方法过滤
        if method:
            filtered_data = [
                record for record in filtered_data
                if record.get('request', {}).get('method', '').upper() == method.upper()
            ]
        
        # 按状态码过滤
        if status_code:
            filtered_data = [
                record for record in filtered_data
                if record.get('response', {}).get('status_code') == status_code
            ]
        
        print(f"\n{Fore.GREEN}🔍 搜索结果: 找到 {len(filtered_data)} 条记录{Style.RESET_ALL}")
        
        for i, record in enumerate(filtered_data[:10]):  # 只显示前10条
            self._print_record_summary(record, i+1)
        
        if len(filtered_data) > 10:
            print(f"{Fore.YELLOW}... 还有 {len(filtered_data)-10} 条记录{Style.RESET_ALL}")
    
    def show_request_detail(self, index):
        """显示请求详情"""
        if not self.data or index < 1 or index > len(self.data):
            print(f"{Fore.RED}❌ 无效的记录索引{Style.RESET_ALL}")
            return
        
        record = self.data[index-1]
        request = record.get('request', {})
        response = record.get('response', {})
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📋 请求详情 #{index}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # 请求信息
        print(f"{Fore.BLUE}📤 请求信息:{Style.RESET_ALL}")
        print(f"  时间: {request.get('timestamp', 'N/A')}")
        print(f"  方法: {request.get('method', 'N/A')}")
        print(f"  URL: {request.get('url', 'N/A')}")
        print(f"  主机: {request.get('host', 'N/A')}")
        print(f"  路径: {request.get('path', 'N/A')}")
        
        # 请求头
        if request.get('headers'):
            print(f"\n{Fore.MAGENTA}📋 请求头:{Style.RESET_ALL}")
            for key, value in request['headers'].items():
                print(f"  {key}: {value}")
        
        # 查询参数
        if request.get('query_params'):
            print(f"\n{Fore.CYAN}🔍 查询参数:{Style.RESET_ALL}")
            print(json.dumps(request['query_params'], ensure_ascii=False, indent=2))
        
        # 请求体
        if request.get('body'):
            print(f"\n{Fore.YELLOW}📦 请求体:{Style.RESET_ALL}")
            if isinstance(request['body'], (dict, list)):
                print(json.dumps(request['body'], ensure_ascii=False, indent=2))
            else:
                print(request['body'])
        
        # 响应信息
        print(f"\n{Fore.BLUE}📥 响应信息:{Style.RESET_ALL}")
        status_color = Fore.GREEN if 200 <= response.get('status_code', 0) < 300 else Fore.RED
        print(f"  状态码: {status_color}{response.get('status_code', 'N/A')} {response.get('status_text', '')}{Style.RESET_ALL}")
        
        # 响应头
        if response.get('headers'):
            print(f"\n{Fore.MAGENTA}📋 响应头:{Style.RESET_ALL}")
            for key, value in response['headers'].items():
                print(f"  {key}: {value}")
        
        # 响应体
        if response.get('body'):
            print(f"\n{Fore.GREEN}📄 响应体:{Style.RESET_ALL}")
            if isinstance(response['body'], (dict, list)):
                print(json.dumps(response['body'], ensure_ascii=False, indent=2))
            else:
                print(str(response['body'])[:1000] + "..." if len(str(response['body'])) > 1000 else response['body'])
    
    def _print_record_summary(self, record, index):
        """打印记录摘要"""
        request = record.get('request', {})
        response = record.get('response', {})
        
        method = request.get('method', 'N/A')
        url = request.get('url', 'N/A')
        status = response.get('status_code', 'N/A')
        timestamp = request.get('timestamp', 'N/A')
        
        status_color = Fore.GREEN if 200 <= status < 300 else Fore.RED if status >= 400 else Fore.YELLOW
        
        print(f"{Fore.CYAN}[{index}]{Style.RESET_ALL} {method} {url}")
        print(f"     状态: {status_color}{status}{Style.RESET_ALL} | 时间: {timestamp}")
    
    def export_summary(self, output_file="api_summary.txt"):
        """导出分析摘要"""
        if not self.data:
            print(f"{Fore.RED}❌ 没有数据可导出{Style.RESET_ALL}")
            return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("API请求分析摘要\n")
            f.write("="*60 + "\n\n")
            
            # 基本统计
            f.write(f"总请求数: {len(self.data)}\n\n")
            
            # 详细记录
            for i, record in enumerate(self.data, 1):
                request = record.get('request', {})
                response = record.get('response', {})
                
                f.write(f"[{i}] {request.get('method', 'N/A')} {request.get('url', 'N/A')}\n")
                f.write(f"    时间: {request.get('timestamp', 'N/A')}\n")
                f.write(f"    状态: {response.get('status_code', 'N/A')}\n")
                
                if request.get('query_params'):
                    f.write(f"    查询参数: {json.dumps(request['query_params'], ensure_ascii=False)}\n")
                
                if request.get('body'):
                    f.write(f"    请求体: {json.dumps(request['body'], ensure_ascii=False) if isinstance(request['body'], (dict, list)) else request['body']}\n")
                
                f.write("\n")
        
        print(f"{Fore.GREEN}✅ 摘要已导出到: {output_file}{Style.RESET_ALL}")

def main():
    """主函数"""
    analyzer = LogAnalyzer()
    
    if not analyzer.load_logs():
        return
    
    while True:
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 API日志分析工具{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. 显示总览统计{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. 搜索请求{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. 查看请求详情{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. 导出摘要{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}5. 重新加载日志{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}0. 退出{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}请选择操作: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            analyzer.analyze_summary()
        elif choice == "2":
            keyword = input(f"{Fore.CYAN}搜索关键词 (可选): {Style.RESET_ALL}").strip() or None
            method = input(f"{Fore.CYAN}请求方法 (可选): {Style.RESET_ALL}").strip() or None
            status = input(f"{Fore.CYAN}状态码 (可选): {Style.RESET_ALL}").strip()
            status_code = int(status) if status.isdigit() else None
            analyzer.search_requests(keyword, method, status_code)
        elif choice == "3":
            index = input(f"{Fore.CYAN}请求记录索引: {Style.RESET_ALL}").strip()
            if index.isdigit():
                analyzer.show_request_detail(int(index))
            else:
                print(f"{Fore.RED}❌ 请输入有效的数字{Style.RESET_ALL}")
        elif choice == "4":
            output_file = input(f"{Fore.CYAN}输出文件名 (默认: api_summary.txt): {Style.RESET_ALL}").strip() or "api_summary.txt"
            analyzer.export_summary(output_file)
        elif choice == "5":
            analyzer.load_logs()
        elif choice == "0":
            print(f"{Fore.GREEN}👋 再见！{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}❌ 无效选择{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 