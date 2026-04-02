#!/usr/bin/env python3
"""
NGT-AI 后端API测试脚本
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_decision_analyze():
    """测试决策分析接口"""
    print("\n🤖 测试决策分析接口...")
    try:
        data = {
            "question": "是否应该投资人工智能技术？",
            "context": "公司正在考虑数字化转型",
            "options": ["立即投资", "观望等待", "暂不投资"],
            "criteria": ["成本效益", "技术风险", "市场机会"]
        }
        response = requests.post(f"{BASE_URL}/api/decision/analyze", json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 决策分析失败: {e}")
        return False

def test_decision_status():
    """测试决策状态接口"""
    print("\n📊 测试决策状态接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/decision/status/temp_decision_123")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 状态查询失败: {e}")
        return False

def test_decision_result():
    """测试决策结果接口"""
    print("\n🎯 测试决策结果接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/decision/result/temp_decision_123")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 结果查询失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("🚀 开始测试 NGT-AI 后端API...")
    print(f"📍 测试地址: {BASE_URL}")
    
    tests = [
        ("健康检查", test_health),
        ("决策分析", test_decision_analyze),
        ("决策状态", test_decision_status),
        ("决策结果", test_decision_result),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"测试: {name}")
        print('='*50)
        result = test_func()
        results.append((name, result))
        time.sleep(1)  # 避免请求过快
    
    print(f"\n{'='*50}")
    print("测试结果汇总")
    print('='*50)
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！后端服务运行正常。")
    else:
        print("⚠️  部分测试失败，请检查服务状态。")

if __name__ == "__main__":
    main()
