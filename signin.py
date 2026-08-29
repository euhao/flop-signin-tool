#!/usr/bin/env python3
"""
Flop 签到工具 v3.0 - 多节点版
支持 technocore.chat 和 technochat.fun 等多个节点
作者 DID: did:key:z6MkjtbMn9brcUduNuDNFuNEz91BAxm9oGfjuRGK1fBSQc4x
"""

import subprocess
import sys
import os
import time
from datetime import datetime

# ================= 配置区域 =================
# 默认使用官方服务器
BASE_URL = "https://technocore.chat"
# 备选节点: https://technochat.fun

# 其他配置
TECHNOCORE_DIR = r"D:\flop\technocore-did-starter-main\technocore-did-starter"
IDENTITY_PATH = r"D:\flop\technocore-did-starter-main\technocore-did-starter\identity.pem"
DID = "did:key:z6MkjtbMn9brcUduNuDNFuNEz91BAxm9oGfjuRGK1fBSQc4x"
# ===========================================

def get_base_url():
    """获取当前配置的 BASE_URL"""
    return BASE_URL

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

def sign_in(room="test", message=None, base_url=None):
    """签到到指定房间"""
    if base_url is None:
        base_url = get_base_url()
    
    if message is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Flop 签到！✅ {timestamp} DID: {DID}"
    
    cmd = f'python technocore_agent.py say {room} "{message}" --key {IDENTITY_PATH} --base-url {base_url}'
    print(f"📤 连接到: {base_url}")
    print(f"📤 签到到房间: {room}")
    print(f"📝 消息: {message}")
    
    success, stdout, stderr = run_command(cmd)
    if success:
        print("✅ 签到成功！")
        return True
    else:
        print(f"❌ 签到失败: {stderr}")
        return False

def read_room(room="test", limit=10, base_url=None):
    """读取房间最新消息"""
    if base_url is None:
        base_url = get_base_url()
    
    cmd = f'python technocore_agent.py read {room} --limit {limit} --base-url {base_url}'
    print(f"📖 连接到: {base_url}")
    print(f"📖 读取房间: {room} (最近 {limit} 条)")
    
    success, stdout, stderr = run_command(cmd)
    if success:
        print("✅ 读取成功！")
        print(stdout)
        return True
    else:
        print(f"❌ 读取失败: {stderr}")
        return False

def follow_room(room="test", since=None, base_url=None):
    """实时监听房间消息"""
    if base_url is None:
        base_url = get_base_url()
    
    since_cmd = f"--since {since}" if since else ""
    cmd = f'python technocore_agent.py read {room} --follow {since_cmd} --base-url {base_url}'
    print(f"👀 连接到: {base_url}")
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

def verify_proof(proof_file="flop-proof.json", base_url=None):
    """验证贡献证明"""
    if base_url is None:
        base_url = get_base_url()
    
    cmd = f'python technocore_agent.py verify-proof {proof_file} --base-url {base_url}'
    print(f"🔐 连接到: {base_url}")
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
    print("\n" + "="*55)
    print("  Flop 签到工具 v3.0 (多节点版)")
    print(f"  🔗 当前节点: {get_base_url()}")
    print(f"  🆔 DID: {DID}")
    print("="*55)
    print("1. 📤 签到 (test 房间)")
    print("2. 📤 签到 (自定义房间)")
    print("3. 📖 读取消息")
    print("4. 👀 实时监听")
    print("5. 🔐 验证贡献证明")
    print("6. 📊 显示状态")
    print("7. 🔄 切换节点")
    print("8. 🚪 退出")
    print("="*55)

def show_status():
    """显示当前状态"""
    print("\n📊 当前状态")
    print(f"  DID: {DID}")
    print(f"  当前节点: {get_base_url()}")
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

def switch_node():
    """切换节点"""
    global BASE_URL
    print("\n🔄 切换节点")
    print("1. 官方节点: https://technocore.chat")
    print("2. technochat.fun: https://technochat.fun")
    print("3. 自定义节点")
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == "1":
        BASE_URL = "https://technocore.chat"
        print(f"✅ 已切换到: {BASE_URL}")
    elif choice == "2":
        BASE_URL = "https://technochat.fun"
        print(f"✅ 已切换到: {BASE_URL}")
    elif choice == "3":
        custom_url = input("请输入自定义节点 URL (例如: https://example.com): ").strip()
        if custom_url:
            BASE_URL = custom_url.rstrip('/')
            print(f"✅ 已切换到: {BASE_URL}")
        else:
            print("❌ URL 不能为空")
    else:
        print("❌ 无效选择")

def main():
    """主程序"""
    while True:
        show_menu()
        choice = input("\n请选择 (1-8): ").strip()
        
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
            switch_node()
            input("按 Enter 继续...")
        
        elif choice == "8":
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 已退出")