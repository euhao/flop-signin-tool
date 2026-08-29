#!/usr/bin/env python3
"""
Flop 签到工具 - Technocore DID 自动化工具
作者 DID: did:key:z6MkjtbMn9brcUduNuDNFuNEz91BAxm9oGfjuRGK1fBSQc4x
"""

import subprocess
import sys
import os
import time
from datetime import datetime

# 配置
TECHNOCORE_DIR = r"D:\flop\technocore-did-starter-main\technocore-did-starter"
IDENTITY_PATH = r"D:\flop\technocore-did-starter-main\technocore-did-starter\identity.pem"
DID = "did:key:z6MkjtbMn9brcUduNuDNFuNEz91BAxm9oGfjuRGK1fBSQc4x"

def run_command(cmd, cwd=TECHNOCORE_DIR):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def sign_in(room="test", message=None):
    """签到到指定房间"""
    if message is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Flop 签到！✅ {timestamp} DID: {DID}"
    
    cmd = f'python technocore_agent.py say {room} "{message}" --key {IDENTITY_PATH}'
    print(f"📤 签到到房间: {room}")
    print(f"📝 消息: {message}")
    
    success, stdout, stderr = run_command(cmd)
    if success:
        print("✅ 签到成功！")
        return True
    else:
        print(f"❌ 签到失败: {stderr}")
        return False

def read_room(room="test", limit=10):
    """读取房间最新消息"""
    cmd = f'python technocore_agent.py read {room} --limit {limit}'
    print(f"📖 读取房间: {room} (最近 {limit} 条)")
    
    success, stdout, stderr = run_command(cmd)
    if success:
        print("✅ 读取成功！")
        print(stdout)
        return True
    else:
        print(f"❌ 读取失败: {stderr}")
        return False

def follow_room(room="test", since=None):
    """实时监听房间消息"""
    since_cmd = f"--since {since}" if since else ""
    cmd = f'python technocore_agent.py read {room} --follow {since_cmd}'
    print(f"👀 实时监听房间: {room} (按 Ctrl+C 退出)")
    
    try:
        subprocess.run(
            cmd,
            shell=True,
            cwd=TECHNOCORE_DIR,
            check=True
        )
    except KeyboardInterrupt:
        print("\n⏹️ 已停止监听")
    except Exception as e:
        print(f"❌ 监听失败: {e}")

def verify_proof(proof_file="flop-proof.json"):
    """验证贡献证明"""
    cmd = f'python technocore_agent.py verify-proof {proof_file}'
    print(f"🔐 验证证明: {proof_file}")
    
    success, stdout, stderr = run_command(cmd)
    if success and "valid proof" in stdout:
        print("✅ 证明有效！")
        print(stdout)
        return True
    else:
        print(f"❌ 证明无效: {stderr}")
        return False

def show_menu():
    """显示主菜单"""
    print("\n" + "="*50)
    print("  Flop 签到工具 v2.0")
    print(f"  DID: {DID}")
    print("="*50)
    print("1. 📤 签到 (test 房间)")
    print("2. 📤 签到 (自定义房间)")
    print("3. 📖 读取消息")
    print("4. 👀 实时监听")
    print("5. 🔐 验证贡献证明")
    print("6. 📊 显示状态")
    print("7. 🚪 退出")
    print("="*50)

def show_status():
    """显示当前状态"""
    print("\n📊 当前状态")
    print(f"  DID: {DID}")
    print(f"  身份文件: {IDENTITY_PATH}")
    print(f"  Technocore 目录: {TECHNOCORE_DIR}")
    
    # 检查身份文件是否存在
    if os.path.exists(IDENTITY_PATH):
        print("  身份状态: ✅ 存在")
    else:
        print("  身份状态: ❌ 未找到")
    
    # 检查证明文件
    proof_path = os.path.join(TECHNOCORE_DIR, "flop-proof.json")
    if os.path.exists(proof_path):
        print("  证明文件: ✅ 存在")
    else:
        print("  证明文件: ❌ 未找到")

def main():
    """主程序"""
    while True:
        show_menu()
        choice = input("\n请选择 (1-7): ").strip()
        
        if choice == "1":
            sign_in()
            input("按 Enter 继续...")
        
        elif choice == "2":
            room = input("请输入房间名: ").strip()
            if room:
                sign_in(room)
            else:
                print("❌ 房间名不能为空")
            input("按 Enter 继续...")
        
        elif choice == "3":
            room = input("请输入房间名 (默认 test): ").strip() or "test"
            limit = input("请输入消息数量 (默认 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            read_room(room, limit)
            input("按 Enter 继续...")
        
        elif choice == "4":
            room = input("请输入房间名 (默认 test): ").strip() or "test"
            since = input("请输入起始序列号 (可选): ").strip()
            since = int(since) if since.isdigit() else None
            follow_room(room, since)
        
        elif choice == "5":
            proof_file = input("请输入证明文件名 (默认 flop-proof.json): ").strip() or "flop-proof.json"
            verify_proof(proof_file)
            input("按 Enter 继续...")
        
        elif choice == "6":
            show_status()
            input("按 Enter 继续...")
        
        elif choice == "7":
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 已退出")