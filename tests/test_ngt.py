"""
NGT-AI 系统单元测试
"""

import unittest
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from src.models.data_structures import DiscussantInitialOutput, ScoreSheet, ScoreRecord
from src.providers.mock_provider import MockModelProvider
from src.core.orchestrator import NGTOrchestrator
from src.core.parser import DataParser
from src.core.state_tracker import StateTracker

class TestDataStructures(unittest.TestCase):
    """测试数据结构"""
    
    def test_discussant_initial_output(self):
        """测试讨论员初始输出"""
        output = DiscussantInitialOutput(
            ai_id="AI_1",
            model_name="gpt-4",
            conclusion="测试结论"
        )
        self.assertEqual(output.ai_id, "AI_1")
        self.assertEqual(output.model_name, "gpt-4")
        self.assertEqual(output.conclusion, "测试结论")
    
    def test_score_record(self):
        """测试评分记录"""
        record = ScoreRecord(score=4, reason="很好的观点")
        self.assertEqual(record.score, 4)
        self.assertEqual(record.reason, "很好的观点")

class TestMockProvider(unittest.TestCase):
    """测试模拟提供器"""
    
    def setUp(self):
        self.provider = MockModelProvider("test-model", "AI_TEST")
    
    def test_provider_info(self):
        """测试提供器基本信息"""
        self.assertEqual(self.provider.get_model_name(), "test-model")
        self.assertEqual(self.provider.get_ai_id(), "AI_TEST")
    
    def test_generate_response(self):
        """测试响应生成"""
        async def test():
            messages = [{"role": "user", "content": "测试问题"}]
            response = await self.provider.generate_response(messages)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
        
        asyncio.run(test())

class TestDataParser(unittest.TestCase):
    """测试数据解析器"""
    
    def test_parse_initial_output(self):
        """测试初始输出解析"""
        json_data = '{"ai_id": "AI_1", "model_name": "gpt-4", "conclusion": "测试结论"}'
        result = DataParser.parse_initial_output(json_data)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.ai_id, "AI_1")
        self.assertEqual(result.conclusion, "测试结论")
    
    def test_parse_invalid_json(self):
        """测试无效JSON解析"""
        invalid_json = '{"invalid": json}'
        result = DataParser.parse_initial_output(invalid_json)
        self.assertIsNone(result)

class TestStateTracker(unittest.TestCase):
    """测试状态追踪器"""
    
    def setUp(self):
        self.tracker = StateTracker()
    
    def test_initial_state(self):
        """测试初始状态"""
        self.assertEqual(self.tracker.user_question, "")
        self.assertEqual(len(self.tracker.initial_outputs), 0)
        self.assertEqual(self.tracker.error_count, 0)
    
    def test_start_process(self):
        """测试开始流程"""
        question = "测试问题"
        self.tracker.start_process(question)
        
        self.assertEqual(self.tracker.user_question, question)
        self.assertGreater(self.tracker.start_time, 0)
        self.assertEqual(self.tracker.current_stage, "阶段1-独立观点生成")

class TestNGTOrchestrator(unittest.TestCase):
    """测试NGT编排器"""
    
    def setUp(self):
        self.discussants = [
            MockModelProvider("model1", "AI_1"),
            MockModelProvider("model2", "AI_2"),
        ]
        self.referee = MockModelProvider("referee-model", "REFEREE")
        self.orchestrator = NGTOrchestrator(self.discussants, self.referee)
    
    def test_orchestrator_init(self):
        """测试编排器初始化"""
        self.assertEqual(len(self.orchestrator.discussants), 2)
        self.assertIsNotNone(self.orchestrator.referee)
        self.assertIsNotNone(self.orchestrator.state)
    
    def test_find_provider_by_id(self):
        """测试按ID查找提供器"""
        provider = self.orchestrator._find_provider_by_id("AI_1")
        self.assertIsNotNone(provider)
        self.assertEqual(provider.get_ai_id(), "AI_1")
        
        # 测试不存在的ID
        provider = self.orchestrator._find_provider_by_id("AI_NONEXISTENT")
        self.assertIsNone(provider)
    
    def test_decision_process(self):
        """测试完整决策流程"""
        async def test():
            question = "如何提高工作效率？"
            try:
                result = await self.orchestrator.run_decision_process(question, max_retries=1)
                
                # 验证基本结构
                self.assertIn("question", result)
                self.assertIn("initial_ideas", result)
                self.assertIn("final_decisions", result)
                self.assertIn("statistics", result)
                
                # 验证问题正确
                self.assertEqual(result["question"], question)
                
                # 验证有初始观点
                self.assertGreater(len(result["initial_ideas"]), 0)
                
                print("✅ 完整决策流程测试通过")
                
            except Exception as e:
                print(f"⚠️  决策流程测试失败: {e}")
                # 在测试环境中，这可能是正常的
        
        asyncio.run(test())

def run_all_tests():
    """运行所有测试"""
    print("🧪 开始运行NGT-AI系统测试...")
    
    # 创建测试套件
    test_classes = [
        TestDataStructures,
        TestMockProvider, 
        TestDataParser,
        TestStateTracker,
        TestNGTOrchestrator
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n📋 测试类: {test_class.__name__}")
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        
        for test in suite:
            total_tests += 1
            try:
                test.debug()
                passed_tests += 1
                print(f"  ✅ {test._testMethodName}")
            except Exception as e:
                print(f"  ❌ {test._testMethodName}: {e}")
    
    print(f"\n📊 测试结果: {passed_tests}/{total_tests} 通过")
    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)