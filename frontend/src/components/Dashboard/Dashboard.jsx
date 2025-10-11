import { useEffect, useMemo, useState } from 'react';
import styles from './Dashboard.module.css';
import TaskSidebar from '../TaskSidebar/TaskSidebar.jsx';
import StageProgress from '../StageProgress/StageProgress.jsx';
import AgentGrid from '../AgentGrid/AgentGrid.jsx';
import DecisionInput from '../DecisionInput/DecisionInput.jsx';
import ReportViewer from '../ReportViewer/ReportViewer.jsx';
import { fetchDecisionResult, fetchDecisionStatus, runDecisionTask } from '../../services/api.js';

const STAGES = ['独立观点', '观点澄清', '交叉评分', '分数聚合', '修正/捍卫', '裁判汇总'];

const INITIAL_PROJECTS = [
  { id: 'proj-core', name: '核心项目', path: 'projects/core/remote-work', summary: '3 个任务进行中' },
  { id: 'proj-lab', name: '创新实验室', path: 'projects/lab/ai-scout', summary: '1 个概念测试' },
  { id: 'proj-quick', name: '快速任务', path: 'projects/inbox', summary: '临时任务收纳' },
];

const INITIAL_TASKS = [
  {
    id: 'task-001',
    title: '制定远程办公安全策略',
    projectId: 'proj-core',
    stageIndex: 4,
    updatedAt: '5 分钟前',
  },
  {
    id: 'task-002',
    title: '新产品市场切入策略',
    projectId: 'proj-core',
    stageIndex: 2,
    updatedAt: '18 分钟前',
  },
  {
    id: 'task-003',
    title: 'AI 客服系统风险评估',
    projectId: 'proj-lab',
    stageIndex: 5,
    updatedAt: '25 分钟前',
  },
];

const INITIAL_FILTERS = [
  { id: 'all', label: '全部', active: true },
  { id: 'in-progress', label: '进行中', active: false },
  { id: 'completed', label: '已完成', active: false },
];

const INITIAL_AGENTS = [
  {
    id: 'AI-1',
    type: 'discussant',
    model: 'gpt-4o',
    prompt: '严谨的战略顾问，专注于可扩展性与执行路径。',
    averageScore: 4.6,
    scoreHistory: [4.2, 4.5, 4.7, 4.8, 4.4, 4.9],
  },
  {
    id: 'AI-2',
    type: 'discussant',
    model: 'gemini-1.5-pro',
    prompt: '以用户体验为核心的产品经理，关注需求洞察。',
    averageScore: 4.3,
    scoreHistory: [3.9, 4.1, 4.6, 4.5, 4.2, 4.4],
  },
  {
    id: 'AI-3',
    type: 'discussant',
    model: 'deepseek-chat',
    prompt: '偏好风险控制的合规专家，审慎评估潜在失误。',
    averageScore: 4.1,
    scoreHistory: [4.0, 3.6, 4.2, 4.4, 4.0, 4.3],
  },
  {
    id: 'AI-4',
    type: 'discussant',
    model: 'qwen-long',
    prompt: '注重创新突破的战略官，勇于提出颠覆方案。',
    averageScore: 4.4,
    scoreHistory: [4.1, 4.6, 4.8, 4.5, 4.3, 4.7],
  },
  {
    id: 'REF',
    type: 'referee',
    model: 'claude-3-opus',
    prompt: '综合全局的裁判，倾向于平衡创新与稳健。',
    averageScore: 4.8,
    scoreHistory: [4.7, 4.8, 4.8, 4.9, 4.8, 5.0],
  },
];

const SAMPLE_REPORT = {
  sections: [
    {
      title: '执行摘要',
      content: '四位讨论员达成一致：采用分阶段推广策略，兼顾产品质量与迭代速度。',
      items: [
        '短期：强化终端管控与员工培训',
        '中期：推进零信任网络与自动化监控',
        '长期：建立跨部门响应机制，持续迭代',
      ],
    },
    {
      title: '亮点观点',
      items: [
        'AI-4 强调创新驱动差异化，同时引入风险缓冲措施。',
        'AI-1 提供清晰的执行节奏与责任矩阵。',
      ],
    },
    {
      title: '风险扫描',
      items: [
        '外部供应链安全：需建立评估与审批流程。',
        '员工合规意识不足：建议建立持续培训机制。',
      ],
    },
    {
      title: '行动建议',
      items: [
        '建立质量红线与快速迭代并行机制。',
        '设立试点验证创新方案并跟踪关键指标。',
      ],
    },
  ],
};

function resolveStageIndex(stageLabel) {
  if (!stageLabel) {
    return null;
  }
  const directMatch = STAGES.indexOf(stageLabel);
  if (directMatch !== -1) {
    return directMatch + 1;
  }
  const match = stageLabel.match(/(\d+)/);
  if (match) {
    const parsed = Number(match[1]);
    if (!Number.isNaN(parsed)) {
      return Math.min(Math.max(parsed, 1), STAGES.length);
    }
  }
  return null;
}

function formatDuration(durationMs) {
  const totalSeconds = Math.floor(durationMs / 1000);
  const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, '0');
  const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0');
  const seconds = String(totalSeconds % 60).padStart(2, '0');
  return `${hours}:${minutes}:${seconds}`;
}

function buildSectionsFromResult(result) {
  if (!result || Object.keys(result).length === 0) {
    return SAMPLE_REPORT;
  }

  const data = result.result_json ?? {};
  const processInfo = data.process_info ?? {};
  const initialIdeas = data.initial_ideas ?? [];
  const finalDecisions = data.final_decisions ?? [];
  const referee = data.referee_analysis ?? {};
  const mergedIdeas = referee.merged_ideas ?? [];
  const highlightedIdeas = referee.highlighted_ideas ?? [];
  const riskSummary = referee.risk_analysis_summary ?? [];

  const sections = [];

  sections.push({
    title: '执行摘要',
    content:
      processInfo.current_stage ??
      '协作流程完成，裁判已提交最终建议。请审阅下方各阶段输出。',
  });

  if (initialIdeas.length > 0) {
    sections.push({
      title: '各讨论员初始观点',
      items: initialIdeas.map((idea) => {
        const modelLabel = idea.model_name ? `（${idea.model_name}）` : '';
        return `${idea.ai_id}${modelLabel}：${idea.conclusion}`;
      }),
    });
  }

  if (referee.final_recommendation || mergedIdeas.length > 0) {
    sections.push({
      title: '裁判综合结论',
      content:
        referee.final_recommendation ??
        '裁判未提供总结性建议，请参考亮点观点与风险评估。',
      items: mergedIdeas.map(
        (idea) => `${idea.merged_idea_id} · 经 ${idea.source_ai_ids.join('、')} 整合：${idea.content}`,
      ),
    });
  }

  if (highlightedIdeas.length > 0) {
    sections.push({
      title: '亮点观点',
      items: highlightedIdeas.map(
        (item) => `${item.source_ai_id}：${item.content}（亮点：${item.reason_for_highlight}）`,
      ),
    });
  }

  if (riskSummary.length > 0) {
    sections.push({
      title: '风险评估建议',
      items: riskSummary.map(
        (item) =>
          `${item.option_id} · 风险等级：${item.risk_level} · 优势：${item.pros.join('，')} · 风险：${item.cons.join('，')}`,
      ),
    });
  }

  if (finalDecisions.length > 0) {
    sections.push({
      title: '行动建议',
      items: finalDecisions.map((decision) => {
        const core =
          decision.final_conclusion ?? decision.defense_statement ?? decision.initial_conclusion;
        const scoreLabel =
          typeof decision.final_score === 'number' ? decision.final_score.toFixed(1) : '—';
        return `${decision.ai_id}（${decision.action}，得分 ${scoreLabel}）：${core}`;
      }),
    });
  }

  return { sections };
}

function Dashboard() {
  const [projects, setProjects] = useState(INITIAL_PROJECTS);
  const [tasks, setTasks] = useState(
    INITIAL_TASKS.map((task) => ({
      ...task,
      stageLabel: `阶段 ${task.stageIndex} · ${STAGES[task.stageIndex - 1]}`,
    })),
  );
  const [activeTaskId, setActiveTaskId] = useState(INITIAL_TASKS[0].id);
  const [filters, setFilters] = useState(INITIAL_FILTERS);
  const [currentStage, setCurrentStage] = useState(3);
  const [elapsed, setElapsed] = useState('00:18:42');
  const [errors, setErrors] = useState(1);
  const [agents, setAgents] = useState(INITIAL_AGENTS);
  const [question, setQuestion] = useState('为全球 2000 人规模的公司设计远程办公政策，兼顾安全、效率与员工体验。');
  const [realtimeApi, setRealtimeApi] = useState(false);
  const [tokensLimit, setTokensLimit] = useState(2048);
  const [report, setReport] = useState(SAMPLE_REPORT);
  const [isRunning, setIsRunning] = useState(false);
  const [decisionId, setDecisionId] = useState(null);

  const activeTask = useMemo(
    () => tasks.find((task) => task.id === activeTaskId),
    [tasks, activeTaskId],
  );

  const handleAddTask = () => {
    const newTask = {
      id: `task-${Math.floor(Math.random() * 10000)}`,
      title: '未命名任务',
      projectId: 'proj-quick',
      stageIndex: 1,
      stageLabel: `阶段 1 · ${STAGES[0]}`,
      updatedAt: '刚刚',
    };

    setTasks((prev) => [newTask, ...prev]);
    setActiveTaskId(newTask.id);
    setCurrentStage(1);
    setElapsed('00:00:00');
    setErrors(0);
    setDecisionId(null);
  };

  const handleRenameProject = (projectId, name) => {
    setProjects((prev) => prev.map((project) => (project.id === projectId ? { ...project, name } : project)));
  };

  const handleToggleFilter = (id) => {
    setFilters((prev) =>
      prev.map((filter) => {
        if (filter.id === 'all') {
          return { ...filter, active: id === 'all' ? !filter.active : false };
        }
        if (filter.id === id) {
          return { ...filter, active: !filter.active };
        }
        return filter;
      }),
    );
  };

  const handleModelChange = (agentId, model) => {
    setAgents((prev) => prev.map((agent) => (agent.id === agentId ? { ...agent, model } : agent)));
  };

  const handlePromptChange = (agentId, prompt) => {
    setAgents((prev) => prev.map((agent) => (agent.id === agentId ? { ...agent, prompt } : agent)));
  };

  const handleRunDecision = async () => {
    if (!question.trim()) {
      return;
    }

    setIsRunning(true);
    setDecisionId(null);
    setCurrentStage(1);
    setElapsed('00:00:05');
    setErrors(0);
    setTasks((prev) =>
      prev.map((task) =>
        task.id === activeTaskId
          ? {
              ...task,
              stageIndex: 1,
              stageLabel: `阶段 1 · ${STAGES[0]}`,
              updatedAt: '刚刚',
            }
          : task,
      ),
    );
    setReport({
      sections: [
        {
          title: '任务已启动',
          content: `任务「${activeTask?.title ?? '新任务'}」正在初始化，智能体即将进入协作阶段。`,
        },
        {
          title: '启动参数',
          items: [
            `实时 API：${realtimeApi ? '启用' : '关闭'}`,
            `Tokens 限制：${tokensLimit}`,
            '可在左侧卡片中调整讨论员模型或提示词。',
          ],
        },
      ],
    });

    try {
      const response = await runDecisionTask({
        question,
        context: '',
        options: [],
        criteria: [],
      });

      const newDecisionId =
        response.decision_id ?? response.decisionId ?? response.id ?? response.task_id ?? null;

      if (newDecisionId) {
        setDecisionId(newDecisionId);
      } else {
        setIsRunning(false);
      }
    } catch (error) {
      console.error('Failed to start decision task', error);
      setErrors((prev) => prev + 1);
      setReport({
        sections: [
          {
            title: '任务启动失败',
            content: '无法连接后端决策服务，请检查网络或稍后重试。',
          },
        ],
      });
      setIsRunning(false);
    }
  };

  const handleClearInput = () => {
    setQuestion('');
  };

  useEffect(() => {
    if (!decisionId) {
      return undefined;
    }

    let cancelled = false;
    const startTime = Date.now();

    const pollStatus = async () => {
      try {
        const status = await fetchDecisionStatus(decisionId);
        if (cancelled) {
          return;
        }

        setElapsed(formatDuration(Date.now() - startTime));

        const resolvedStage = resolveStageIndex(status.stage);
        if (resolvedStage) {
          setCurrentStage(resolvedStage);
          setTasks((prev) =>
            prev.map((task) =>
              task.id === activeTaskId
                ? {
                    ...task,
                    stageIndex: resolvedStage,
                    stageLabel: `阶段 ${resolvedStage} · ${STAGES[resolvedStage - 1]}`,
                    updatedAt: '刚刚',
                  }
                : task,
            ),
          );
        }

        if (typeof status.error_count === 'number') {
          setErrors(status.error_count);
        }

        if (status.status === 'completed' || status.status === 'failed') {
          const result = await fetchDecisionResult(decisionId);
          if (!cancelled) {
            setReport(buildSectionsFromResult(result));
            setCurrentStage(STAGES.length);
            setIsRunning(false);
            setDecisionId(null);
          }
        }
      } catch (error) {
        console.error('Polling decision status failed', error);
      }
    };

    const interval = setInterval(pollStatus, 4000);
    pollStatus();

    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [decisionId, activeTaskId]);

  return (
    <div className={styles.dashboard}>
      <div className={styles.sidebarArea}>
        <TaskSidebar
          tasks={tasks}
          projects={projects}
          activeTaskId={activeTaskId}
          onSelectTask={setActiveTaskId}
          onAddTask={handleAddTask}
          filters={filters}
          onToggleFilter={handleToggleFilter}
          onRenameProject={handleRenameProject}
        />
      </div>

      <div className={styles.mainArea}>
        <div className={styles.progressArea}>
          <StageProgress currentStage={currentStage} stages={STAGES} elapsed={elapsed} errors={errors} />
        </div>

        <div className={styles.controlsArea}>
          <div className={styles.agentsArea}>
            <AgentGrid agents={agents} onModelChange={handleModelChange} onPromptChange={handlePromptChange} />
          </div>
          <div className={styles.inputArea}>
            <DecisionInput
              value={question}
              onChange={setQuestion}
              onRun={handleRunDecision}
              onClear={handleClearInput}
              realtimeApi={realtimeApi}
              onToggleRealtimeApi={setRealtimeApi}
              tokensLimit={tokensLimit}
              onTokensLimitChange={setTokensLimit}
              isRunning={isRunning}
            />
          </div>
        </div>

        <div className={styles.reportArea}>
          <ReportViewer
            report={report}
            onExport={() => window.alert('导出功能开发中')}
            onCopy={() => window.alert('复制功能开发中')}
            onToggleTheme={() => window.alert('主题切换功能开发中')}
          />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
