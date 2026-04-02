export const SUPPORTED_LANGUAGES = [
  { code: 'zh', label: '中文' },
  { code: 'en', label: 'English' },
  { code: 'ja', label: '日本語' },
  { code: 'fr', label: 'Français' },
];

export const translations = {
  zh: {
    'language.label': '语言',
    'stageProgress.title': '任务进度',
    'stageProgress.elapsed': '已用时',
    'stageProgress.errors': '错误',
    'stageProgress.language': '界面语言',

    'auth.login.title': '欢迎回来',
    'auth.login.subtitle': '请登录以继续使用 NGT-AI 决策中心',
    'auth.login.email': '邮箱',
    'auth.login.password': '密码',
    'auth.login.identifier': '手机号 / 邮箱',
    'auth.login.identifierPlaceholder': '请输入手机号或邮箱',
    'auth.login.identifierRequired': '请填写手机号或邮箱',
    'auth.hero.badge': '多智能体·NGT流程',
    'auth.hero.title': '欢迎来到 NGT-AI',
    'auth.hero.subtitle': '多智能体并行思考与交叉评审，让每个决策都有充分论证。',
    'auth.hero.point1': '多智能体并行思考与交叉评审，让每个决策都有充分论证。',
    'auth.hero.point2': '可视化展示整个 NGT 思维链路，从生成到汇总一目了然。',
    'auth.hero.point3': '支持邮箱 / 手机 登录，一键启动智能决策。',
    'auth.hero.footer': '登录即表示同意我们的服务条款与隐私政策。',
    'auth.login.nickname': '昵称',
    'auth.login.nicknamePlaceholder': '可选，用于个性化展示',
    'auth.login.submit': '登录',
    'auth.login.register': '创建账号',
    'auth.login.submitting': '处理中...',
    'auth.login.switchToRegister': '还没有账号？立即注册',
    'auth.login.switchToLogin': '已经有账号？直接登录',
    'auth.login.error': '无法完成登录，请稍后再试',
    'auth.login.altHint': '提示：请使用真实联系方式，方便接收系统通知。',

    'dashboard.stages.stage1': '独立观点',
    'dashboard.stages.stage2': '观点澄清',
    'dashboard.stages.stage3': '交叉评分',
    'dashboard.stages.stage4': '分数聚合',
    'dashboard.stages.stage5': '修正/捍卫',
    'dashboard.stages.stage6': '裁判汇总',

    'dashboard.projects.core.name': '核心项目',
    'dashboard.projects.core.summary': '3 个任务进行中',
    'dashboard.projects.lab.name': '创新实验室',
    'dashboard.projects.lab.summary': '1 个概念测试',
    'dashboard.projects.quick.name': '快速任务',
    'dashboard.projects.quick.summary': '临时任务收纳',

    'dashboard.tasks.task1.title': '制定远程办公安全策略',
    'dashboard.tasks.task1.updated': '5 分钟前',
    'dashboard.tasks.task2.title': '新产品市场切入策略',
    'dashboard.tasks.task2.updated': '18 分钟前',
    'dashboard.tasks.task3.title': 'AI 客服系统风险评估',
    'dashboard.tasks.task3.updated': '25 分钟前',

    'dashboard.filters.all': '全部',
    'dashboard.filters.inProgress': '进行中',
    'dashboard.filters.completed': '已完成',

    'dashboard.agents.discussant1.prompt': '严谨的战略顾问，专注于可扩展性与执行路径。',
    'dashboard.agents.discussant2.prompt': '以用户体验为核心的产品经理，关注需求洞察。',
    'dashboard.agents.discussant3.prompt': '偏好风险控制的合规专家，审慎评估潜在失误。',
    'dashboard.agents.discussant4.prompt': '注重创新突破的战略官，勇于提出颠覆方案。',
    'dashboard.agents.referee.prompt': '综合全局的裁判，倾向于平衡创新与稳健。',

    'dashboard.sampleReport.summary.title': '执行摘要',
    'dashboard.sampleReport.summary.content':
      '四位讨论员达成一致：采用分阶段推广策略，兼顾产品质量与迭代速度。',
    'dashboard.sampleReport.summary.item1': '短期：强化终端管控与员工培训',
    'dashboard.sampleReport.summary.item2': '中期：推进零信任网络与自动化监控',
    'dashboard.sampleReport.summary.item3': '长期：建立跨部门响应机制，持续迭代',
    'dashboard.sampleReport.highlights.title': '亮点观点',
    'dashboard.sampleReport.highlights.item1': 'AI-4 强调创新驱动差异化，同时引入风险缓冲措施。',
    'dashboard.sampleReport.highlights.item2': 'AI-1 提供清晰的执行节奏与责任矩阵。',
    'dashboard.sampleReport.risk.title': '风险扫描',
    'dashboard.sampleReport.risk.item1': '外部供应链安全：需建立评估与审批流程。',
    'dashboard.sampleReport.risk.item2': '员工合规意识不足：建议建立持续培训机制。',
    'dashboard.sampleReport.actions.title': '行动建议',
    'dashboard.sampleReport.actions.item1': '建立质量红线与快速迭代并行机制。',
    'dashboard.sampleReport.actions.item2': '设立试点验证创新方案并跟踪关键指标。',

    'dashboard.stageLabel': '阶段 {number} · {stage}',
    'dashboard.initialQuestion': '为全球 2000 人规模的公司设计远程办公政策，兼顾安全、效率与员工体验。',
    'dashboard.tasks.untitled': '未命名任务',
    'dashboard.tasks.justNow': '刚刚',

    'dashboard.run.startedTitle': '任务已启动',
    'dashboard.run.startedContent': '任务「{task}」正在初始化，智能体即将进入协作阶段。',
    'dashboard.run.newTaskPlaceholder': '新任务',
    'dashboard.run.startParamsTitle': '启动参数',
    'dashboard.run.paramRealtime': '实时 API：{status}',
    'dashboard.common.enabled': '启用',
    'dashboard.common.disabled': '关闭',
    'dashboard.run.paramTokens': 'Tokens 限制：{limit}',
    'dashboard.run.adjustAgentsHint': '可以在左侧卡片中调整模型或提示词配置。',
    'dashboard.run.validation.questionTooShort': '请先输入至少 5 个字符的问题，再启动决策流程。',
    'dashboard.run.failedTitle': '任务启动失败',
    'dashboard.run.failedContent': '无法连接后端决策服务，请检查网络或稍后重试。',

    'dashboard.alert.exportPending': '导出功能开发中',
    'dashboard.alert.copyPending': '复制功能开发中',
    'dashboard.alert.themePending': '主题切换功能开发中',
    'dashboard.header.title': 'NGT-AI 决策中心',
    'dashboard.header.subtitle': '多智能体协作，快速生成洞见',
    'userMenu.anonymous': '访客用户',
    'userMenu.manage': '账户设置',
    'userMenu.manageUnavailable': '账户设置功能即将上线',
    'userMenu.logout': '退出登录',

    'sidebar.renameProjectPrompt': '重命名项目',
    'sidebar.renameProjectAria': '重命名 {name}',
    'sidebar.title': '决策任务',
    'sidebar.addTask': '添加任务',
    'sidebar.addProject': '添加项目',
    'sidebar.deleteProjectConfirm': '确认删除该项目及其所有任务？',
    'sidebar.deleteTaskConfirm': '确认删除该任务？',
    'sidebar.loading': '正在同步任务...',
    'sidebar.stageUnknown': '等待执行',
    'sidebar.projects': '项目',
    'sidebar.emptyProject': '暂无任务，点击右上角添加或在运行后生成。',
    'sidebar.orphanTasks': '未归档任务',
    'sidebar.systemOnline': '系统在线',
    'sidebar.taskCount': '任务数：{count}',

    'agentGrid.title': '多智能体配置',
    'agentGrid.discussant': '讨论员',
    'agentGrid.referee': '裁判',

    'agentCard.promptLabel': '角色提示',
    'agentCard.averageScore': '平均得分',

    'decisionInput.label': '输入决策问题',
    'decisionInput.placeholder': '描述需要协作分析的问题、背景与目标...',
    'decisionInput.clear': '清除',
    'decisionInput.run': '运行决策',
    'decisionInput.running': '运行中...',
    'decisionInput.realtime': '实时 API',
    'decisionInput.tokensLimit': 'Tokens 限制',

    'reportViewer.title': '协作报告',
    'reportViewer.export': '导出',
    'reportViewer.copy': '复制',
    'reportViewer.theme': '主题',
    'reportViewer.waiting': '等待新的输出',
    'reportViewer.emptyTitle': '尚未生成任何报告',
    'reportViewer.emptyHint': '运行一次决策任务后，这里会展示完整的协作结果。',

    'dashboard.report.summary.title': '执行摘要',
    'dashboard.report.summary.contentDefault':
      '协作流程完成，裁判已提交最终建议。请审阅下方各阶段输出。',
    'dashboard.report.summary.metric.duration': '处理时长: {value}',
    'dashboard.report.summary.metric.participants': '参与AI数量: {value}',
    'dashboard.report.summary.metric.initialIdeas': '初始观点数: {value}',
    'dashboard.report.summary.metric.revisedCount': '观点修正数: {value}',
    'dashboard.report.summary.metric.defendedCount': '观点捍卫数: {value}',
    'dashboard.report.summary.metric.averageScore': '平均得分: {value}',
    'dashboard.report.summary.metric.completionRate': '完成率: {value}',
    'dashboard.report.summary.metric.errorCount': '错误次数: {value}',

    'dashboard.report.initialIdeas.title': '各讨论员初始观点',
    'dashboard.report.initialIdeas.entry': '{ai}{modelLabel}：{conclusion}',
    'dashboard.report.initialIdeas.modelLabel': '（{model}）',

    'dashboard.report.scoring.title': '交叉评分详情',
    'dashboard.report.scoring.entry': '{scorer} 的评分：{scores}',

    'dashboard.report.referee.title': '裁判综合结论',
    'dashboard.report.referee.fallback': '裁判未提供总结性建议，请参考亮点观点与风险评估。',
    'dashboard.report.referee.entry': '{id} · 经 {sources} 整合：{content}',

    'dashboard.report.highlights.title': '亮点观点',
    'dashboard.report.highlights.entry': '{ai}：{content}（亮点：{reason}）',

    'dashboard.report.risk.title': '风险评估建议',
    'dashboard.report.risk.entry': '{option} · 风险等级：{level} · 优势：{pros} · 风险：{cons}',

    'dashboard.report.actions.title': '行动建议',
    'dashboard.report.actions.entry': '{ai}（{action}，得分 {score}）：{content}',
    'dashboard.report.actions.action.revised': '修正',
    'dashboard.report.actions.action.defended': '捍卫',
  },

  en: {
    'language.label': 'Language',
    'stageProgress.title': 'Stage Progress',
    'stageProgress.elapsed': 'Elapsed',
    'stageProgress.errors': 'Errors',
    'stageProgress.language': 'Interface language',

    'auth.login.title': 'Welcome back',
    'auth.login.subtitle': 'Sign in to continue with the NGT-AI control center.',
    'auth.login.email': 'Email',
    'auth.login.password': 'Password',
    'auth.login.identifier': 'Phone or email',
    'auth.login.identifierPlaceholder': 'Enter phone number or email',
    'auth.login.identifierRequired': 'Please provide a phone number or email.',
    'auth.hero.badge': 'NGT · Multimodel',
    'auth.hero.title': 'Return to NGT-AI',
    'auth.hero.subtitle': 'NGT-AI distills collective intelligence into a serene, reliable workspace.',
    'auth.hero.point1': 'Trace the entire NGT loop with cinematic clarity.',
    'auth.hero.point2': 'Sign in once across corporate email or phone.',
    'auth.hero.point3': 'Data stays in your region with local-first storage.',
    'auth.hero.footer': 'By signing in you agree to our Terms and Privacy Policy.',
    'auth.login.nickname': 'Display name',
    'auth.login.nicknamePlaceholder': 'Optional – helps personalise your workspace',
    'auth.login.submit': 'Sign in',
    'auth.login.register': 'Create account',
    'auth.login.submitting': 'Processing...',
    'auth.login.switchToRegister': 'No account yet? Create one',
    'auth.login.switchToLogin': 'Already have an account? Sign in',
    'auth.login.error': 'Unable to complete the request. Please try again later.',
    'auth.login.altHint': 'Tip: use a valid contact so we can reach you about decisions.',

    'dashboard.stages.stage1': 'Independent Ideas',
    'dashboard.stages.stage2': 'Clarify Ideas',
    'dashboard.stages.stage3': 'Cross-Scoring',
    'dashboard.stages.stage4': 'Score Aggregation',
    'dashboard.stages.stage5': 'Revise / Defend',
    'dashboard.stages.stage6': 'Referee Synthesis',

    'dashboard.projects.core.name': 'Core Program',
    'dashboard.projects.core.summary': '3 tasks in progress',
    'dashboard.projects.lab.name': 'Innovation Lab',
    'dashboard.projects.lab.summary': '1 concept test',
    'dashboard.projects.quick.name': 'Quick Inbox',
    'dashboard.projects.quick.summary': 'Temporary task inbox',

    'dashboard.tasks.task1.title': 'Design remote-work security policy',
    'dashboard.tasks.task1.updated': '5 minutes ago',
    'dashboard.tasks.task2.title': 'New product market entry strategy',
    'dashboard.tasks.task2.updated': '18 minutes ago',
    'dashboard.tasks.task3.title': 'AI support system risk assessment',
    'dashboard.tasks.task3.updated': '25 minutes ago',

    'dashboard.filters.all': 'All',
    'dashboard.filters.inProgress': 'In progress',
    'dashboard.filters.completed': 'Completed',

    'dashboard.agents.discussant1.prompt':
      'A meticulous strategy advisor focused on scalability and executable roadmaps.',
    'dashboard.agents.discussant2.prompt':
      'A product manager centred on user experience with sharp demand insights.',
    'dashboard.agents.discussant3.prompt':
      'A compliance expert who prioritises risk control and spots hidden pitfalls.',
    'dashboard.agents.discussant4.prompt':
      'A strategy officer pursuing disruptive innovation with bold proposals.',
    'dashboard.agents.referee.prompt':
      'A holistic referee balancing innovation with operational stability.',

    'dashboard.sampleReport.summary.title': 'Executive summary',
    'dashboard.sampleReport.summary.content':
      'All four discussants recommend a phased rollout balancing product quality with iteration speed.',
    'dashboard.sampleReport.summary.item1': 'Short term: reinforce endpoint control and staff training',
    'dashboard.sampleReport.summary.item2': 'Mid term: advance zero-trust networking and automated monitoring',
    'dashboard.sampleReport.summary.item3': 'Long term: build cross-team response loops with continuous iteration',
    'dashboard.sampleReport.highlights.title': 'Highlights',
    'dashboard.sampleReport.highlights.item1':
      'AI-4 emphasises innovation-led differentiation while adding risk buffers.',
    'dashboard.sampleReport.highlights.item2':
      'AI-1 outlines a clear execution cadence and responsibility matrix.',
    'dashboard.sampleReport.risk.title': 'Risk scan',
    'dashboard.sampleReport.risk.item1': 'External supply-chain security: establish assessment and approval steps.',
    'dashboard.sampleReport.risk.item2':
      'Employee compliance awareness: launch ongoing enablement and coaching.',
    'dashboard.sampleReport.actions.title': 'Recommended actions',
    'dashboard.sampleReport.actions.item1':
      'Run quality guardrails alongside rapid iteration to keep release confidence.',
    'dashboard.sampleReport.actions.item2':
      'Pilot innovative ideas and track leading indicators before global rollout.',

    'dashboard.stageLabel': 'Stage {number} · {stage}',
    'dashboard.initialQuestion':
      'Design a remote-work policy for a 2,000-person global company that balances security, efficiency, and employee experience.',
    'dashboard.tasks.untitled': 'Untitled task',
    'dashboard.tasks.justNow': 'Just now',

    'dashboard.run.startedTitle': 'Task started',
    'dashboard.run.startedContent':
      'Task “{task}” is initialising and agents are switching into collaboration.',
    'dashboard.run.newTaskPlaceholder': 'New task',
    'dashboard.run.startParamsTitle': 'Launch parameters',
    'dashboard.run.paramRealtime': 'Realtime API: {status}',
    'dashboard.common.enabled': 'Enabled',
    'dashboard.common.disabled': 'Disabled',
    'dashboard.run.paramTokens': 'Token limit: {limit}',
    'dashboard.run.adjustAgentsHint': 'Adjust agent models or prompts using the cards on the left.',
    'dashboard.run.validation.questionTooShort': 'Please enter at least 5 characters before starting a decision.',
    'dashboard.run.failedTitle': 'Task failed to start',
    'dashboard.run.failedContent':
      'Unable to reach the decision service. Please check connectivity and try again.',

    'dashboard.alert.exportPending': 'Export is coming soon',
    'dashboard.alert.copyPending': 'Copy feature is coming soon',
    'dashboard.alert.themePending': 'Theme switching is coming soon',
    'dashboard.header.title': 'NGT-AI Decision Hub',
    'dashboard.header.subtitle': 'Coordinate AI teammates to surface better insights.',
    'userMenu.anonymous': 'Guest',
    'userMenu.manage': 'Account settings',
    'userMenu.manageUnavailable': 'Account settings will be available soon.',
    'userMenu.logout': 'Sign out',

    'sidebar.renameProjectPrompt': 'Rename project',
    'sidebar.renameProjectAria': 'Rename {name}',
    'sidebar.title': 'Decision tasks',
    'sidebar.addTask': 'Add task',
    'sidebar.addProject': 'Add project',
    'sidebar.deleteProjectConfirm': 'Delete this project and all of its tasks?',
    'sidebar.deleteTaskConfirm': 'Delete this task?',
    'sidebar.loading': 'Syncing workspace...',
    'sidebar.stageUnknown': 'Pending',
    'sidebar.projects': 'Projects',
    'sidebar.emptyProject': 'No tasks yet. Click the plus button or run a decision to generate one.',
    'sidebar.orphanTasks': 'Unfiled tasks',
    'sidebar.systemOnline': 'System online',
    'sidebar.taskCount': 'Tasks: {count}',

    'agentGrid.title': 'Multi-agent configuration',
    'agentGrid.discussant': 'Discussant',
    'agentGrid.referee': 'Referee',

    'agentCard.promptLabel': 'Role prompt',
    'agentCard.averageScore': 'Average score',

    'decisionInput.label': 'Enter the decision question',
    'decisionInput.placeholder':
      'Describe the challenge, context, and objective that need collaborative analysis...',
    'decisionInput.clear': 'Clear',
    'decisionInput.run': 'Run decision',
    'decisionInput.running': 'Running...',
    'decisionInput.realtime': 'Realtime API',
    'decisionInput.tokensLimit': 'Token limit',

    'reportViewer.title': 'Collaboration report',
    'reportViewer.export': 'Export',
    'reportViewer.copy': 'Copy',
    'reportViewer.theme': 'Theme',
    'reportViewer.waiting': 'Waiting for new output',
    'reportViewer.emptyTitle': 'No report yet',
    'reportViewer.emptyHint':
      'Run a decision task to generate the collaborative report, which will appear here.',

    'dashboard.report.summary.title': 'Executive summary',
    'dashboard.report.summary.contentDefault':
      'The workflow has completed and the referee submitted final recommendations. Review each phase below.',
    'dashboard.report.summary.metric.duration': 'Duration: {value}',
    'dashboard.report.summary.metric.participants': 'Participating AIs: {value}',
    'dashboard.report.summary.metric.initialIdeas': 'Initial ideas: {value}',
    'dashboard.report.summary.metric.revisedCount': 'Revisions: {value}',
    'dashboard.report.summary.metric.defendedCount': 'Defences: {value}',
    'dashboard.report.summary.metric.averageScore': 'Average score: {value}',
    'dashboard.report.summary.metric.completionRate': 'Completion rate: {value}',
    'dashboard.report.summary.metric.errorCount': 'Errors: {value}',

    'dashboard.report.initialIdeas.title': 'Initial ideas by discussant',
    'dashboard.report.initialIdeas.entry': '{ai}{modelLabel}: {conclusion}',
    'dashboard.report.initialIdeas.modelLabel': ' ({model})',

    'dashboard.report.scoring.title': 'Cross-scoring details',
    'dashboard.report.scoring.entry': '{scorer} scored: {scores}',

    'dashboard.report.referee.title': 'Referee synthesis',
    'dashboard.report.referee.fallback':
      'No summary from the referee. Refer to highlights and risk assessment instead.',
    'dashboard.report.referee.entry': '{id} · merged from {sources}: {content}',

    'dashboard.report.highlights.title': 'Highlights',
    'dashboard.report.highlights.entry': '{ai}: {content} (Highlight: {reason})',

    'dashboard.report.risk.title': 'Risk assessment',
    'dashboard.report.risk.entry': '{option} · Risk level: {level} · Pros: {pros} · Cons: {cons}',

    'dashboard.report.actions.title': 'Recommended actions',
    'dashboard.report.actions.entry': '{ai} ({action}, score {score}): {content}',
    'dashboard.report.actions.action.revised': 'Revised',
    'dashboard.report.actions.action.defended': 'Defended',
  },

  ja: {
    'language.label': '言語',
    'stageProgress.title': '進捗状況',
    'stageProgress.elapsed': '経過時間',
    'stageProgress.errors': 'エラー',
    'stageProgress.language': '表示言語',

    'auth.login.title': 'お帰りなさい',
    'auth.login.subtitle': 'NGT-AI コントロールセンターにログインしてください。',
    'auth.login.email': 'メールアドレス',
    'auth.login.password': 'パスワード',
    'auth.login.identifier': '電話番号 / メールアドレス',
    'auth.login.identifierPlaceholder': '電話番号またはメールアドレスを入力してください',
    'auth.login.identifierRequired': '電話番号またはメールアドレスを入力してください。',
    'auth.hero.badge': 'NGT · マルチエージェント',
    'auth.hero.title': 'NGT-AI へようこそ',
    'auth.hero.subtitle': 'NGT-AI はマルチエージェント協調を静かに、確実に支援する専用空間です。',
    'auth.hero.point1': 'NGT の各フェーズをシネマティックに可視化',
    'auth.hero.point2': '企業メール / 電話番号でシームレスにログイン',
    'auth.hero.point3': 'ローカル優先のデータ管理で安心・安全',
    'auth.hero.footer': 'ログインすると利用規約とプライバシーポリシーに同意したことになります。',
    'auth.login.nickname': '表示名',
    'auth.login.nicknamePlaceholder': '任意 — ワークスペースでの表示に使用されます',
    'auth.login.submit': 'ログイン',
    'auth.login.register': 'アカウントを作成',
    'auth.login.submitting': '処理中…',
    'auth.login.switchToRegister': 'アカウントが必要ですか？今すぐ登録',
    'auth.login.switchToLogin': 'すでに登録済みですか？ログイン',
    'auth.login.error': 'ログインに失敗しました。しばらくしてから再度お試しください。',
    'auth.login.altHint': '注意：連絡可能な情報を入力すると通知を受け取りやすくなります。',


    'dashboard.stages.stage1': '独立アイデア',
    'dashboard.stages.stage2': 'アイデア整理',
    'dashboard.stages.stage3': 'クロス評価',
    'dashboard.stages.stage4': 'スコア集約',
    'dashboard.stages.stage5': '修正／弁護',
    'dashboard.stages.stage6': '審判統合',

    'dashboard.projects.core.name': '中核プロジェクト',
    'dashboard.projects.core.summary': '進行中のタスク 3 件',
    'dashboard.projects.lab.name': 'イノベーションラボ',
    'dashboard.projects.lab.summary': '概念検証 1 件',
    'dashboard.projects.quick.name': 'クイックタスク',
    'dashboard.projects.quick.summary': '臨時タスクの受け皿',

    'dashboard.tasks.task1.title': 'リモートワークのセキュリティ方針策定',
    'dashboard.tasks.task1.updated': '5 分前',
    'dashboard.tasks.task2.title': '新製品の市場参入戦略',
    'dashboard.tasks.task2.updated': '18 分前',
    'dashboard.tasks.task3.title': 'AI カスタマーサービスのリスク評価',
    'dashboard.tasks.task3.updated': '25 分前',

    'dashboard.filters.all': 'すべて',
    'dashboard.filters.inProgress': '進行中',
    'dashboard.filters.completed': '完了',

    'dashboard.agents.discussant1.prompt':
      'スケーラビリティと実行計画にこだわる綿密な戦略アドバイザー。',
    'dashboard.agents.discussant2.prompt':
      'ユーザー体験を軸に洞察を掘り下げるプロダクトマネージャー。',
    'dashboard.agents.discussant3.prompt':
      'リスク統制を重視し潜在的な失敗を慎重に見極めるコンプライアンス専門家。',
    'dashboard.agents.discussant4.prompt':
      '大胆な提案で破壊的イノベーションを目指す戦略オフィサー。',
    'dashboard.agents.referee.prompt':
      '革新と安定のバランスを取る全体俯瞰型の審判役。',

    'dashboard.sampleReport.summary.title': 'エグゼクティブサマリー',
    'dashboard.sampleReport.summary.content':
      '4 名の討議者は段階的な展開を推奨し、品質と iteration スピードの両立を提案しています。',
    'dashboard.sampleReport.summary.item1': '短期：エンドポイント管理と社員トレーニングを強化',
    'dashboard.sampleReport.summary.item2': '中期：ゼロトラスト網と自動監視を推進',
    'dashboard.sampleReport.summary.item3': '長期：部門横断の対応体制を整備し継続的に改善',
    'dashboard.sampleReport.highlights.title': '注目ポイント',
    'dashboard.sampleReport.highlights.item1':
      'AI-4 は差別化を生むイノベーションとリスク緩和策の両立を主張。',
    'dashboard.sampleReport.highlights.item2': 'AI-1 は実行リズムと責任分担を明確に提示。',
    'dashboard.sampleReport.risk.title': 'リスク分析',
    'dashboard.sampleReport.risk.item1': '外部サプライチェーンの安全性：評価と承認プロセスの構築が必要。',
    'dashboard.sampleReport.risk.item2': '社員のコンプライアンス意識：継続的なトレーニング体制を推奨。',
    'dashboard.sampleReport.actions.title': 'アクション提案',
    'dashboard.sampleReport.actions.item1': '品質基準と高速な反復を両立させる仕組みを構築。',
    'dashboard.sampleReport.actions.item2': 'パイロットで革新的な案を検証し主要指標を追跡。',

    'dashboard.stageLabel': 'ステージ {number} · {stage}',
    'dashboard.initialQuestion':
      '世界 2000 人規模の企業向けに、安全性・効率・従業員体験を両立するリモートワーク方針を設計してください。',
    'dashboard.tasks.untitled': '名称未設定のタスク',
    'dashboard.tasks.justNow': 'たった今',

    'dashboard.run.startedTitle': 'タスクが開始されました',
    'dashboard.run.startedContent': '「{task}」が初期化され、エージェントが協調モードに入ります。',
    'dashboard.run.newTaskPlaceholder': '新規タスク',
    'dashboard.run.startParamsTitle': '起動パラメータ',
    'dashboard.run.paramRealtime': 'リアルタイム API：{status}',
    'dashboard.common.enabled': '有効',
    'dashboard.common.disabled': '無効',
    'dashboard.run.paramTokens': 'トークン上限: {limit}',
    'dashboard.run.adjustAgentsHint': '左側のカードからモデルやプロンプトを調整できます。',
    'dashboard.run.validation.questionTooShort': '決定を実行する前に5文字以上で質問を入力してください。',
    'dashboard.run.failedTitle': 'タスクの起動に失敗しました',
    'dashboard.run.failedContent': '意思決定サービスに接続できません。ネットワークを確認のうえ再試行してください。',

    'dashboard.alert.exportPending': 'エクスポート機能は準備中です',
    'dashboard.alert.copyPending': 'コピー機能は準備中です',
    'dashboard.alert.themePending': 'テーマ切り替え機能は準備中です',
    'dashboard.header.title': 'NGT-AI 意思決定ハブ',
    'dashboard.header.subtitle': '専門AIを連携させ、優れた洞察を引き出します。',
    'userMenu.anonymous': 'ゲストユーザー',
    'userMenu.manage': 'アカウント設定',
    'userMenu.manageUnavailable': 'アカウント設定機能はまもなく公開予定です。',
    'userMenu.logout': 'ログアウト',

    'sidebar.renameProjectPrompt': 'プロジェクト名を変更',
    'sidebar.renameProjectAria': '{name} の名前を変更',
    'sidebar.title': '意思決定タスク',
    'sidebar.addTask': 'タスクを追加',
    'sidebar.addProject': 'プロジェクトを追加',
    'sidebar.deleteProjectConfirm': 'このプロジェクトとすべてのタスクを削除しますか？',
    'sidebar.deleteTaskConfirm': 'このタスクを削除しますか？',
    'sidebar.loading': 'ワークスペースを同期しています...',
    'sidebar.stageUnknown': '待機中',
    'sidebar.projects': 'プロジェクト',
    'sidebar.emptyProject': 'タスクがありません。右上のボタンを押すか、決定を実行して生成してください。',
    'sidebar.orphanTasks': '未整理のタスク',
    'sidebar.systemOnline': 'システムオンライン',
    'sidebar.taskCount': 'タスク数: {count}',

    'agentGrid.title': 'マルチエージェント設定',
    'agentGrid.discussant': '討議者',
    'agentGrid.referee': '審判',

    'agentCard.promptLabel': '役割プロンプト',
    'agentCard.averageScore': '平均スコア',

    'decisionInput.label': '意思決定の課題を入力',
    'decisionInput.placeholder': '協調分析したい課題や背景、目標を記述してください...',
    'decisionInput.clear': 'クリア',
    'decisionInput.run': '意思決定を実行',
    'decisionInput.running': '実行中...',
    'decisionInput.realtime': 'リアルタイム API',
    'decisionInput.tokensLimit': 'トークン上限',

    'reportViewer.title': '協調レポート',
    'reportViewer.export': 'エクスポート',
    'reportViewer.copy': 'コピー',
    'reportViewer.theme': 'テーマ',
    'reportViewer.waiting': '新しい出力を待機中',
    'reportViewer.emptyTitle': 'レポートはまだありません',
    'reportViewer.emptyHint': '意思決定タスクを実行すると、ここに協調結果が表示されます。',

    'dashboard.report.summary.title': 'エグゼクティブサマリー',
    'dashboard.report.summary.contentDefault':
      'ワークフローが完了し、審判が最終提案を提出しました。以下の各段階を確認してください。',
    'dashboard.report.summary.metric.duration': '処理時間: {value}',
    'dashboard.report.summary.metric.participants': '参加 AI 数: {value}',
    'dashboard.report.summary.metric.initialIdeas': '初期アイデア数: {value}',
    'dashboard.report.summary.metric.revisedCount': '修正数: {value}',
    'dashboard.report.summary.metric.defendedCount': '弁護数: {value}',
    'dashboard.report.summary.metric.averageScore': '平均スコア: {value}',
    'dashboard.report.summary.metric.completionRate': '完了率: {value}',
    'dashboard.report.summary.metric.errorCount': 'エラー数: {value}',

    'dashboard.report.initialIdeas.title': '討議者の初期アイデア',
    'dashboard.report.initialIdeas.entry': '{ai}{modelLabel}: {conclusion}',
    'dashboard.report.initialIdeas.modelLabel': '（{model}）',

    'dashboard.report.scoring.title': 'クロス評価の詳細',
    'dashboard.report.scoring.entry': '{scorer} の評価: {scores}',

    'dashboard.report.referee.title': '審判による統合結論',
    'dashboard.report.referee.fallback': '審判のサマリーはありません。ハイライトとリスク評価を参照してください。',
    'dashboard.report.referee.entry': '{id} · {sources} を統合: {content}',

    'dashboard.report.highlights.title': 'ハイライト',
    'dashboard.report.highlights.entry': '{ai}: {content}（ハイライト: {reason}）',

    'dashboard.report.risk.title': 'リスク評価',
    'dashboard.report.risk.entry': '{option} · リスクレベル: {level} · 長所: {pros} · リスク: {cons}',

    'dashboard.report.actions.title': '推奨アクション',
    'dashboard.report.actions.entry': '{ai}（{action}、スコア {score}）: {content}',
    'dashboard.report.actions.action.revised': '修正',
    'dashboard.report.actions.action.defended': '弁護',
  },

  fr: {
    'language.label': 'Langue',
    'stageProgress.title': 'Progression',
    'stageProgress.elapsed': 'Durée',
    'stageProgress.errors': 'Erreurs',
    'stageProgress.language': 'Langue de l’interface',

    'auth.login.title': 'Bienvenue',
    'auth.login.subtitle': 'Connectez-vous pour continuer sur la console NGT-AI.',
    'auth.login.email': 'Email',
    'auth.login.password': 'Mot de passe',
    'auth.login.identifier': 'Téléphone ou e-mail',
    'auth.login.identifierPlaceholder': 'Saisissez votre numéro ou email',
    'auth.login.identifierRequired': 'Merci d’indiquer un numéro ou un email.',
    'auth.hero.badge': 'NGT · Intelligence collective',
    'auth.hero.title': 'Bienvenue sur NGT-AI',
    'auth.hero.subtitle': 'NGT-AI concentre l’intelligence collective dans un espace calme et fiable.',
    'auth.hero.point1': 'Visualisez chaque phase du protocole NGT.',
    'auth.hero.point2': 'Connexion unique via email professionnel ou mobile.',
    'auth.hero.point3': 'Stockage local-first pour garder la maîtrise de vos données.',
    'auth.hero.footer': 'En vous connectant, vous acceptez nos CGU et notre politique de confidentialité.',
    'auth.login.nickname': 'Nom affiché',
    'auth.login.nicknamePlaceholder': 'Facultatif — personnalise votre espace',
    'auth.login.submit': 'Se connecter',
    'auth.login.register': 'Créer un compte',
    'auth.login.submitting': 'Traitement…',
    'auth.login.switchToRegister': 'Pas encore de compte ? Inscrivez-vous',
    'auth.login.switchToLogin': 'Déjà inscrit ? Connectez-vous',
    'auth.login.error': 'Impossible de terminer la requête pour le moment.',
    'auth.login.altHint': 'Astuce : utilisez un contact valide pour recevoir les notifications.',

    'dashboard.stages.stage1': 'Idées indépendantes',
    'dashboard.stages.stage2': 'Clarification des idées',
    'dashboard.stages.stage3': 'Évaluation croisée',
    'dashboard.stages.stage4': 'Agrégation des scores',
    'dashboard.stages.stage5': 'Révision / Défense',
    'dashboard.stages.stage6': 'Synthèse de l’arbitre',

    'dashboard.projects.core.name': 'Projet central',
    'dashboard.projects.core.summary': '3 tâches en cours',
    'dashboard.projects.lab.name': 'Laboratoire d’innovation',
    'dashboard.projects.lab.summary': '1 test de concept',
    'dashboard.projects.quick.name': 'Tâches rapides',
    'dashboard.projects.quick.summary': 'Boîte des tâches temporaires',

    'dashboard.tasks.task1.title': 'Définir une politique de sécurité du télétravail',
    'dashboard.tasks.task1.updated': 'Il y a 5 minutes',
    'dashboard.tasks.task2.title': 'Stratégie d’entrée sur le marché du nouveau produit',
    'dashboard.tasks.task2.updated': 'Il y a 18 minutes',
    'dashboard.tasks.task3.title': 'Évaluer les risques du support client IA',
    'dashboard.tasks.task3.updated': 'Il y a 25 minutes',

    'dashboard.filters.all': 'Toutes',
    'dashboard.filters.inProgress': 'En cours',
    'dashboard.filters.completed': 'Terminées',

    'dashboard.agents.discussant1.prompt':
      'Conseiller stratégique méticuleux, focalisé sur l’évolutivité et la feuille de route.',
    'dashboard.agents.discussant2.prompt':
      'Chef de produit centré sur l’expérience utilisateur et la détection fine des besoins.',
    'dashboard.agents.discussant3.prompt':
      'Expert conformité orienté maîtrise des risques et prévention des erreurs latentes.',
    'dashboard.agents.discussant4.prompt':
      'Responsable stratégique en quête d’innovations de rupture et de paris audacieux.',
    'dashboard.agents.referee.prompt':
      'Arbitre global privilégiant l’équilibre entre innovation et robustesse.',

    'dashboard.sampleReport.summary.title': 'Synthèse exécutive',
    'dashboard.sampleReport.summary.content':
      'Les quatre intervenants recommandent un déploiement progressif conciliant qualité et vitesse d’itération.',
    'dashboard.sampleReport.summary.item1': 'Court terme : renforcer le contrôle des terminaux et la formation',
    'dashboard.sampleReport.summary.item2': 'Moyen terme : déployer le zéro confiance et la surveillance automatisée',
    'dashboard.sampleReport.summary.item3': 'Long terme : structurer une coordination inter-équipes et itérer en continu',
    'dashboard.sampleReport.highlights.title': 'Points marquants',
    'dashboard.sampleReport.highlights.item1':
      'AI-4 met l’accent sur une différenciation par l’innovation avec amortisseurs de risque.',
    'dashboard.sampleReport.highlights.item2':
      'AI-1 propose un rythme d’exécution clair avec une matrice de responsabilités.',
    'dashboard.sampleReport.risk.title': 'Analyse des risques',
    'dashboard.sampleReport.risk.item1':
      'Sécurité de la chaîne d’approvisionnement : instaurer un processus d’évaluation et d’approbation.',
    'dashboard.sampleReport.risk.item2':
      'Sensibilisation des collaborateurs : mettre en place une formation continue.',
    'dashboard.sampleReport.actions.title': 'Actions recommandées',
    'dashboard.sampleReport.actions.item1':
      'Maintenir des garde-fous qualité tout en itérant rapidement.',
    'dashboard.sampleReport.actions.item2':
      'Piloter des projets pilotes innovants et suivre les indicateurs clés avant extension.',

    'dashboard.stageLabel': 'Étape {number} · {stage}',
    'dashboard.initialQuestion':
      'Concevez une politique de télétravail pour une entreprise mondiale de 2 000 personnes conciliant sécurité, efficacité et expérience employé.',
    'dashboard.tasks.untitled': 'Tâche sans titre',
    'dashboard.tasks.justNow': 'À l’instant',

    'dashboard.run.startedTitle': 'Tâche lancée',
    'dashboard.run.startedContent':
      'La tâche « {task} » est en cours d’initialisation ; les agents passent en mode collaboration.',
    'dashboard.run.newTaskPlaceholder': 'Nouvelle tâche',
    'dashboard.run.startParamsTitle': 'Paramètres de démarrage',
    'dashboard.run.paramRealtime': 'API temps réel : {status}',
    'dashboard.common.enabled': 'Activé',
    'dashboard.common.disabled': 'Désactivé',
    'dashboard.run.paramTokens': 'Limite de jetons : {limit}',
    'dashboard.run.adjustAgentsHint': 'Ajustez les modèles ou prompts via les cartes à gauche.',
    'dashboard.run.validation.questionTooShort': 'Veuillez saisir au moins 5 caractères avant de lancer une décision.',
    'dashboard.run.failedTitle': 'Échec du lancement',
    'dashboard.run.failedContent':
      'Impossible de joindre le service de décision. Vérifiez la connexion puis réessayez.',

    'dashboard.alert.exportPending': 'Exportation en cours de préparation',
    'dashboard.alert.copyPending': 'Fonction de copie en cours de préparation',
    'dashboard.alert.themePending': 'Changement de thème en cours de préparation',
    'dashboard.header.title': 'Plateforme de décision NGT-AI',
    'dashboard.header.subtitle': 'Coordonnez des experts IA pour obtenir de meilleures idées plus rapidement.',
    'userMenu.anonymous': 'Invité',
    'userMenu.manage': 'Paramètres du compte',
    'userMenu.manageUnavailable': 'Les paramètres du compte seront disponibles prochainement.',
    'userMenu.logout': 'Se déconnecter',

    'sidebar.renameProjectPrompt': 'Renommer le projet',
    'sidebar.renameProjectAria': 'Renommer {name}',
    'sidebar.title': 'Tâches de décision',
    'sidebar.addTask': 'Ajouter une tâche',
    'sidebar.addProject': 'Ajouter un projet',
    'sidebar.deleteProjectConfirm': 'Supprimer ce projet et toutes ses tâches ?',
    'sidebar.deleteTaskConfirm': 'Supprimer cette tâche ?',
    'sidebar.loading': 'Synchronisation de l’espace de travail...',
    'sidebar.stageUnknown': 'En attente',
    'sidebar.projects': 'Projets',
    'sidebar.emptyProject':
      'Aucune tâche pour le moment. Cliquez sur le bouton plus ou exécutez une décision pour en générer une.',
    'sidebar.orphanTasks': 'Tâches non classées',
    'sidebar.systemOnline': 'Système en ligne',
    'sidebar.taskCount': 'Tâches : {count}',

    'agentGrid.title': 'Configuration multi-agents',
    'agentGrid.discussant': 'Intervenant',
    'agentGrid.referee': 'Arbitre',

    'agentCard.promptLabel': 'Prompt de rôle',
    'agentCard.averageScore': 'Score moyen',

    'decisionInput.label': 'Saisir la question de décision',
    'decisionInput.placeholder':
      'Décrivez le problème à analyser, son contexte et l’objectif recherché...',
    'decisionInput.clear': 'Effacer',
    'decisionInput.run': 'Lancer la décision',
    'decisionInput.running': 'Exécution...',
    'decisionInput.realtime': 'API temps réel',
    'decisionInput.tokensLimit': 'Limite de jetons',

    'reportViewer.title': 'Rapport de collaboration',
    'reportViewer.export': 'Exporter',
    'reportViewer.copy': 'Copier',
    'reportViewer.theme': 'Thème',
    'reportViewer.waiting': 'En attente d’un nouveau résultat',
    'reportViewer.emptyTitle': 'Aucun rapport pour le moment',
    'reportViewer.emptyHint':
      'Lancez une décision pour générer le rapport collaboratif qui s’affichera ici.',

    'dashboard.report.summary.title': 'Synthèse exécutive',
    'dashboard.report.summary.contentDefault':
      'Le processus est achevé et l’arbitre a remis sa recommandation. Consultez les étapes ci-dessous.',
    'dashboard.report.summary.metric.duration': 'Durée : {value}',
    'dashboard.report.summary.metric.participants': 'IA participantes : {value}',
    'dashboard.report.summary.metric.initialIdeas': 'Idées initiales : {value}',
    'dashboard.report.summary.metric.revisedCount': 'Révisions : {value}',
    'dashboard.report.summary.metric.defendedCount': 'Défenses : {value}',
    'dashboard.report.summary.metric.averageScore': 'Score moyen : {value}',
    'dashboard.report.summary.metric.completionRate': 'Taux d’achèvement : {value}',
    'dashboard.report.summary.metric.errorCount': 'Erreurs : {value}',

    'dashboard.report.initialIdeas.title': 'Idées initiales par intervenant',
    'dashboard.report.initialIdeas.entry': '{ai}{modelLabel} : {conclusion}',
    'dashboard.report.initialIdeas.modelLabel': ' ({model})',

    'dashboard.report.scoring.title': 'Détails de l’évaluation croisée',
    'dashboard.report.scoring.entry': 'Évaluation de {scorer} : {scores}',

    'dashboard.report.referee.title': 'Synthèse de l’arbitre',
    'dashboard.report.referee.fallback':
      'Aucune synthèse n’a été fournie. Reportez-vous aux points forts et à l’analyse des risques.',
    'dashboard.report.referee.entry': '{id} · Fusion de {sources} : {content}',

    'dashboard.report.highlights.title': 'Points forts',
    'dashboard.report.highlights.entry': '{ai} : {content} (Point fort : {reason})',

    'dashboard.report.risk.title': 'Analyse des risques',
    'dashboard.report.risk.entry': '{option} · Niveau de risque : {level} · Atouts : {pros} · Risques : {cons}',

    'dashboard.report.actions.title': 'Actions recommandées',
    'dashboard.report.actions.entry': '{ai} ({action}, score {score}) : {content}',
    'dashboard.report.actions.action.revised': 'Révisé',
    'dashboard.report.actions.action.defended': 'Défendu',
  },
};

export function getLocaleFromLanguage(language) {
  switch (language) {
    case 'zh':
      return 'zh-CN';
    case 'ja':
      return 'ja-JP';
    case 'fr':
      return 'fr-FR';
    default:
      return 'en-US';
  }
}
