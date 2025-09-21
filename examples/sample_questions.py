"""
NGT-AI 系统示例问题集
"""

# 商业决策类问题
BUSINESS_QUESTIONS = [
    "我们公司应该如何制定远程工作政策？",
    "新产品的定价策略应该如何设定？", 
    "如何提升客户满意度和忠诚度？",
    "公司数字化转型的优先级应该如何排序？",
    "如何平衡成本控制与业务增长？",
    "团队扩张时应该优先招聘哪类人才？",
    "如何建立有效的绩效考核体系？",
    "公司文化建设的关键措施有哪些？"
]

# 个人发展类问题
PERSONAL_QUESTIONS = [
    "如何在工作与生活之间找到更好的平衡？",
    "职业发展规划应该考虑哪些因素？",
    "如何提升个人学习效率和知识管理？",
    "选择职业方向时应该重点考虑什么？",
    "如何建立和维护专业人脉网络？",
    "时间管理的最佳实践方法是什么？",
    "如何克服工作中的拖延症？",
    "持续学习的动力和方法有哪些？"
]

# 技术决策类问题
TECHNICAL_QUESTIONS = [
    "选择技术栈时应该考虑哪些因素？",
    "如何设计可扩展的系统架构？",
    "代码质量管理的最佳实践是什么？",
    "如何平衡技术债务与新功能开发？",
    "团队协作工具的选择标准有哪些？",
    "如何建立有效的代码审查流程？",
    "数据安全和隐私保护的关键措施？",
    "如何评估和选择第三方服务？"
]

# 创新策略类问题
INNOVATION_QUESTIONS = [
    "如何培养团队的创新思维和能力？",
    "新兴技术的采用时机如何把握？",
    "如何建立创新项目的评估体系？",
    "跨界合作的机会和风险如何评估？",
    "如何平衡创新投入与风险控制？",
    "用户需求挖掘和验证的有效方法？",
    "如何建立学习型组织文化？",
    "面对颠覆性变化时的应对策略？"
]

# 所有问题集合
ALL_QUESTIONS = (
    BUSINESS_QUESTIONS + 
    PERSONAL_QUESTIONS + 
    TECHNICAL_QUESTIONS + 
    INNOVATION_QUESTIONS
)

def get_random_question(category=None):
    """获取随机问题"""
    import random
    
    if category == "business":
        return random.choice(BUSINESS_QUESTIONS)
    elif category == "personal": 
        return random.choice(PERSONAL_QUESTIONS)
    elif category == "technical":
        return random.choice(TECHNICAL_QUESTIONS)
    elif category == "innovation":
        return random.choice(INNOVATION_QUESTIONS)
    else:
        return random.choice(ALL_QUESTIONS)

def get_questions_by_category():
    """按类别获取所有问题"""
    return {
        "商业决策": BUSINESS_QUESTIONS,
        "个人发展": PERSONAL_QUESTIONS, 
        "技术决策": TECHNICAL_QUESTIONS,
        "创新策略": INNOVATION_QUESTIONS
    }

def demo_questions():
    """演示问题集"""
    print("🎯 NGT-AI 示例问题集")
    print("=" * 50)
    
    categories = get_questions_by_category()
    
    for category, questions in categories.items():
        print(f"\n📋 {category} ({len(questions)}个问题)")
        for i, question in enumerate(questions, 1):
            print(f"  {i}. {question}")
    
    print(f"\n📊 总计: {len(ALL_QUESTIONS)} 个示例问题")

if __name__ == "__main__":
    demo_questions()