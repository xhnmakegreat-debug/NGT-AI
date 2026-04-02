import { useCallback, useEffect, useMemo, useState } from 'react';
import styles from './Dashboard.module.css';
import TaskSidebar from '../TaskSidebar/TaskSidebar.jsx';
import StageProgress from '../StageProgress/StageProgress.jsx';
import AgentGrid from '../AgentGrid/AgentGrid.jsx';
import DecisionInput from '../DecisionInput/DecisionInput.jsx';
import ReportViewer from '../ReportViewer/ReportViewer.jsx';
import {
  fetchDecisionResult,
  fetchDecisionStatus,
  fetchWorkspace,
  runDecisionTask,
  createProject,
  updateProject,
  deleteProject,
  createTask,
  deleteTask,
} from '../../services/api.js';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import { useAuth } from '../../context/AuthContext.jsx';

const STAGE_KEYS = [
  'dashboard.stages.stage1',
  'dashboard.stages.stage2',
  'dashboard.stages.stage3',
  'dashboard.stages.stage4',
  'dashboard.stages.stage5',
  'dashboard.stages.stage6',
];

const AGENT_TEMPLATES = [
  {
    id: 'AI-1',
    type: 'discussant',
    model: 'gpt-4o',
    promptKey: 'dashboard.agents.discussant1.prompt',
    averageScore: 4.6,
    scoreHistory: [4.2, 4.5, 4.7, 4.8, 4.4, 4.9],
  },
  {
    id: 'AI-2',
    type: 'discussant',
    model: 'gemini-1.5-pro',
    promptKey: 'dashboard.agents.discussant2.prompt',
    averageScore: 4.3,
    scoreHistory: [3.9, 4.1, 4.6, 4.5, 4.2, 4.4],
  },
  {
    id: 'AI-3',
    type: 'discussant',
    model: 'deepseek-chat',
    promptKey: 'dashboard.agents.discussant3.prompt',
    averageScore: 4.1,
    scoreHistory: [4.0, 3.6, 4.2, 4.4, 4.0, 4.3],
  },
  {
    id: 'AI-4',
    type: 'discussant',
    model: 'qwen-long',
    promptKey: 'dashboard.agents.discussant4.prompt',
    averageScore: 4.4,
    scoreHistory: [4.1, 4.6, 4.8, 4.5, 4.3, 4.7],
  },
  {
    id: 'REF',
    type: 'referee',
    model: 'claude-3-opus',
    promptKey: 'dashboard.agents.referee.prompt',
    averageScore: 4.8,
    scoreHistory: [4.7, 4.8, 4.8, 4.9, 4.8, 5.0],
  },
];

function createInitialAgents(t) {
  return AGENT_TEMPLATES.map((template) => ({
    ...template,
    prompt: t(template.promptKey),
    promptKey: template.promptKey,
    customPrompt: false,
  }));
}

function createSampleReport(t) {
  return {
    isPlaceholder: true,
    sections: [
      {
        title: t('dashboard.sampleReport.summary.title'),
        content: t('dashboard.sampleReport.summary.content'),
        items: [
          t('dashboard.sampleReport.summary.item1'),
          t('dashboard.sampleReport.summary.item2'),
          t('dashboard.sampleReport.summary.item3'),
        ],
      },
      {
        title: t('dashboard.sampleReport.highlights.title'),
        items: [
          t('dashboard.sampleReport.highlights.item1'),
          t('dashboard.sampleReport.highlights.item2'),
        ],
      },
      {
        title: t('dashboard.sampleReport.risk.title'),
        items: [
          t('dashboard.sampleReport.risk.item1'),
          t('dashboard.sampleReport.risk.item2'),
        ],
      },
      {
        title: t('dashboard.sampleReport.actions.title'),
        items: [
          t('dashboard.sampleReport.actions.item1'),
          t('dashboard.sampleReport.actions.item2'),
        ],
      },
    ],
  };
}

function formatDuration(durationMs) {
  const totalSeconds = Math.floor(durationMs / 1000);
  const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, '0');
  const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0');
  const seconds = String(totalSeconds % 60).padStart(2, '0');
  return `${hours}:${minutes}:${seconds}`;
}

function resolveStageIndex(stageLabel, stageNames) {
  if (!stageLabel) {
    return null;
  }
  const directMatch = stageNames.indexOf(stageLabel);
  if (directMatch !== -1) {
    return directMatch + 1;
  }
  const match = stageLabel.match(/(\d+)/);
  if (match) {
    const parsed = Number(match[1]);
    if (!Number.isNaN(parsed)) {
      return Math.min(Math.max(parsed, 1), stageNames.length);
    }
  }
  return null;
}

function formatList(items, formatter) {
  if (!Array.isArray(items) || items.length === 0) {
    return '—';
  }
  return formatter.format(items);
}

function buildSectionsFromResult(result, t, locale) {
  if (!result || Object.keys(result).length === 0) {
    return createSampleReport(t);
  }

  const data = result.result_json ?? {};
  const processInfo = data.process_info ?? {};
  const initialIdeas = data.initial_ideas ?? [];
  const finalDecisions = data.final_decisions ?? [];
  const referee = data.referee_analysis ?? {};
  const mergedIdeas = referee.merged_ideas ?? [];
  const highlightedIdeas = referee.highlighted_ideas ?? [];
  const riskSummary = referee.risk_analysis_summary ?? [];
  const stats = data.statistics || {};

  const listFormatter = new Intl.ListFormat(locale, { style: 'long', type: 'conjunction' });

  const sections = [];

  const summaryItems = [
    t('dashboard.report.summary.metric.duration', {
      value: data.process_duration || 'N/A',
    }),
    t('dashboard.report.summary.metric.participants', {
      value: data.participants?.total ?? 'N/A',
    }),
    t('dashboard.report.summary.metric.initialIdeas', {
      value: stats.total_ideas ?? 0,
    }),
    t('dashboard.report.summary.metric.revisedCount', {
      value: stats.revised_count ?? 0,
    }),
    t('dashboard.report.summary.metric.defendedCount', {
      value: stats.defended_count ?? 0,
    }),
    t('dashboard.report.summary.metric.averageScore', {
      value: `${stats.average_score ?? 0}/100`,
    }),
    t('dashboard.report.summary.metric.completionRate', {
      value: `${((stats.completion_rate ?? 0) * 100).toFixed(1)}%`,
    }),
    t('dashboard.report.summary.metric.errorCount', {
      value: stats.error_count ?? 0,
    }),
  ];

  sections.push({
    title: t('dashboard.report.summary.title'),
    content: processInfo.current_stage ?? t('dashboard.report.summary.contentDefault'),
    items: summaryItems,
  });

  if (initialIdeas.length > 0) {
    sections.push({
      title: t('dashboard.report.initialIdeas.title'),
      items: initialIdeas.map((idea) => {
        const modelLabel = idea.model_name
          ? t('dashboard.report.initialIdeas.modelLabel', { model: idea.model_name })
          : '';
        return t('dashboard.report.initialIdeas.entry', {
          ai: idea.ai_id,
          modelLabel,
          conclusion: idea.conclusion,
        });
      }),
    });
  }

  if (Array.isArray(data.score_sheets) && data.score_sheets.length > 0) {
    sections.push({
      title: t('dashboard.report.scoring.title'),
      items: data.score_sheets.map((sheet) => {
        const scores = Object.entries(sheet.scores || {})
          .filter(([, score]) => score !== null)
          .map(([aiId, score]) => `${aiId}: ${score.score}/5 (${score.reason})`)
          .join('; ');
        return t('dashboard.report.scoring.entry', {
          scorer: sheet.scorer_ai_id,
          scores,
        });
      }),
    });
  }

  if (referee.final_recommendation || mergedIdeas.length > 0) {
    sections.push({
      title: t('dashboard.report.referee.title'),
      content: referee.final_recommendation ?? t('dashboard.report.referee.fallback'),
      items: mergedIdeas.map((idea) =>
        t('dashboard.report.referee.entry', {
          id: idea.merged_idea_id,
          sources: formatList(idea.source_ai_ids ?? [], listFormatter),
          content: idea.content,
        }),
      ),
    });
  }

  if (highlightedIdeas.length > 0) {
    sections.push({
      title: t('dashboard.report.highlights.title'),
      items: highlightedIdeas.map((idea) =>
        t('dashboard.report.highlights.entry', {
          ai: idea.source_ai_id,
          content: idea.content,
          reason: idea.reason_for_highlight,
        }),
      ),
    });
  }

  if (riskSummary.length > 0) {
    sections.push({
      title: t('dashboard.report.risk.title'),
      items: riskSummary.map((risk) =>
        t('dashboard.report.risk.entry', {
          option: risk.option_id,
          level: risk.risk_level,
          pros: formatList(risk.pros, listFormatter),
          cons: formatList(risk.cons, listFormatter),
        }),
      ),
    });
  }

  if (finalDecisions.length > 0) {
    sections.push({
      title: t('dashboard.report.actions.title'),
      items: finalDecisions.map((decision) =>
        t('dashboard.report.actions.entry', {
          ai: decision.ai_id,
          action:
            decision.action === 'REVISED'
              ? t('dashboard.report.actions.action.revised')
              : t('dashboard.report.actions.action.defended'),
          score: decision.final_score.toFixed(1),
          content:
            decision.action === 'REVISED'
              ? decision.final_conclusion
              : decision.defense_statement ?? decision.initial_conclusion,
        }),
      ),
    });
  }

  return {
    isPlaceholder: false,
    sections,
  };
}

function flattenTasks(projects) {
  return projects.flatMap((project) =>
    (project.tasks ?? []).map((task) => ({
      ...task,
      projectId: project.id,
      projectName: project.name,
    })),
  );
}

function generateProjectName(question) {
  const base = question?.trim() ? question.trim().slice(0, 16) : 'Quick project';
  const now = new Date();
  const stamp = `${now.getHours().toString().padStart(2, '0')}${now
    .getMinutes()
    .toString()
    .padStart(2, '0')}${now.getSeconds().toString().padStart(2, '0')}`;
  const entropy = Math.random().toString(36).slice(-3).toUpperCase();
  return `${base} · ${stamp}${entropy}`;
}

function generateTaskTitle(question) {
  const base = question?.trim() ? question.trim().slice(0, 32) : 'New task';
  const suffix = Math.random().toString(36).slice(-2).toUpperCase();
  return `${base} #${suffix}`;
}

function Dashboard() {
  const { t, language, locale } = useLanguage();
  const { user, isAuthenticated } = useAuth();

  const stages = useMemo(() => STAGE_KEYS.map((key) => t(key)), [t]);

  const [projects, setProjects] = useState([]);
  const [activeTaskId, setActiveTaskId] = useState(null);
  const [workspaceLoading, setWorkspaceLoading] = useState(false);
  const [workspaceError, setWorkspaceError] = useState(null);
  const [currentStage, setCurrentStage] = useState(1);
  const [elapsed, setElapsed] = useState('00:00:00');
  const [errors, setErrors] = useState(0);
  const [agents, setAgents] = useState(() => createInitialAgents(t));
  const [question, setQuestion] = useState(t('dashboard.initialQuestion'));
  const [realtimeApi, setRealtimeApi] = useState(false);
  const [tokensLimit, setTokensLimit] = useState(2048);
  const [report, setReport] = useState(() => createSampleReport(t));
  const [isRunning, setIsRunning] = useState(false);
  const [activeRun, setActiveRun] = useState(null);

  const allTasks = useMemo(() => flattenTasks(projects), [projects]);
  const activeTask = useMemo(
    () => allTasks.find((task) => task.id === activeTaskId) ?? null,
    [allTasks, activeTaskId],
  );

  const ensureAuthenticated = useCallback(() => {
    if (!isAuthenticated) {
      window.alert(t('dashboard.run.failedTitle'));
      return false;
    }
    return true;
  }, [isAuthenticated, t]);

  const refreshWorkspace = useCallback(
    async (preferredTaskId = null) => {
      if (!isAuthenticated) {
        return;
      }
      setWorkspaceLoading(true);
      setWorkspaceError(null);
      try {
        const snapshot = await fetchWorkspace();
        const projectList = Array.isArray(snapshot?.projects) ? snapshot.projects : [];
        setProjects(projectList);
        const tasks = flattenTasks(projectList);
        let nextTaskId = preferredTaskId ?? activeTaskId;
        if (nextTaskId && !tasks.some((task) => task.id === nextTaskId)) {
          nextTaskId = null;
        }
        if (!nextTaskId) {
          nextTaskId = tasks[0]?.id ?? null;
        }
        setActiveTaskId(nextTaskId);
      } catch (error) {
        console.error('Failed to load workspace', error);
        setWorkspaceError(error.message ?? 'Failed to sync workspace');
      } finally {
        setWorkspaceLoading(false);
      }
    },
    [isAuthenticated, activeTaskId],
  );

  const updateTaskProgress = useCallback((taskId, partial) => {
    if (!taskId) {
      return;
    }
    setProjects((prev) =>
      prev.map((project) => {
        if (!project.tasks?.some((task) => task.id === taskId)) {
          return project;
        }
        return {
          ...project,
          tasks: project.tasks.map((task) => (task.id === taskId ? { ...task, ...partial } : task)),
        };
      }),
    );
  }, []);

  useEffect(() => {
    if (!isAuthenticated) {
      setProjects([]);
      setActiveTaskId(null);
      setActiveRun(null);
      setWorkspaceError(null);
      setIsRunning(false);
      setCurrentStage(1);
      setElapsed('00:00:00');
      setErrors(0);
      setQuestion(t('dashboard.initialQuestion'));
      setReport(createSampleReport(t));
      return;
    }
    refreshWorkspace();
  }, [isAuthenticated, user?.id, t, refreshWorkspace]);

  useEffect(() => {
    setAgents((prev) =>
      prev.map((agent) => {
        const template = AGENT_TEMPLATES.find((item) => item.id === agent.id);
        if (!template || agent.customPrompt) {
          return agent;
        }
        return {
          ...agent,
          prompt: t(template.promptKey),
        };
      }),
    );
  }, [language, t]);

  useEffect(() => {
    setReport((prev) => (prev?.isPlaceholder ? createSampleReport(t) : prev));
  }, [language, t]);

  const handleModelChange = useCallback((agentId, model) => {
    setAgents((prev) =>
      prev.map((agent) => (agent.id === agentId ? { ...agent, model } : agent)),
    );
  }, []);

  const handlePromptChange = useCallback((agentId, prompt) => {
    setAgents((prev) =>
      prev.map((agent) =>
        agent.id === agentId ? { ...agent, prompt, customPrompt: true } : agent,
      ),
    );
  }, []);

  const handleAddProject = async () => {
    if (!ensureAuthenticated()) return;
    const name = window.prompt(t('sidebar.renameProjectPrompt'));
    if (!name || !name.trim()) {
      return;
    }
    try {
      await createProject({ name: name.trim() });
      await refreshWorkspace();
    } catch (error) {
      console.error('Create project failed', error);
      window.alert(t('dashboard.run.failedTitle'));
    }
  };

  const handleRenameProject = async (projectId, currentName) => {
    if (!ensureAuthenticated()) return;
    const nextName = window.prompt(t('sidebar.renameProjectPrompt'), currentName);
    if (!nextName || !nextName.trim() || nextName.trim() === currentName) {
      return;
    }
    try {
      const updated = await updateProject(projectId, { name: nextName.trim() });
      setProjects((prev) => prev.map((project) => (project.id === updated.id ? updated : project)));
    } catch (error) {
      console.error('Rename project failed', error);
      window.alert(t('dashboard.run.failedTitle'));
    }
  };

  const handleDeleteProject = async (projectId) => {
    if (!ensureAuthenticated()) return;
    if (!window.confirm(t('sidebar.deleteProjectConfirm'))) {
      return;
    }
    try {
      await deleteProject(projectId);
      const fallbackTask = activeTaskId && activeTask?.projectId === projectId ? null : activeTaskId;
      await refreshWorkspace(fallbackTask);
    } catch (error) {
      console.error('Delete project failed', error);
      window.alert(t('dashboard.run.failedTitle'));
    }
  };

  const handleAddTask = async (projectId) => {
    if (!ensureAuthenticated()) return;
    const title = window.prompt(
      t('dashboard.run.newTaskPlaceholder'),
      generateTaskTitle(question),
    );
    if (!title || !title.trim()) {
      return;
    }
    try {
      const task = await createTask(projectId, { title: title.trim() });
      await refreshWorkspace(task.id);
    } catch (error) {
      console.error('Create task failed', error);
      window.alert(t('dashboard.run.failedTitle'));
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!ensureAuthenticated()) return;
    if (!window.confirm(t('sidebar.deleteTaskConfirm'))) {
      return;
    }
    try {
      await deleteTask(taskId);
      await refreshWorkspace(activeTaskId === taskId ? null : activeTaskId);
    } catch (error) {
      console.error('Delete task failed', error);
      window.alert(t('dashboard.run.failedTitle'));
    }
  };

  const handleRunDecision = async () => {
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion) {
      return;
    }
    if (trimmedQuestion.length < 5) {
      window.alert(t('dashboard.run.validation.questionTooShort'));
      return;
    }
    if (!ensureAuthenticated()) {
      return;
    }

    setIsRunning(true);
    setCurrentStage(1);
    setElapsed('00:00:05');
    setErrors(0);
    setReport({
      isPlaceholder: true,
      sections: [
        {
          title: t('dashboard.run.startedTitle'),
          content: t('dashboard.run.startedContent', {
            task: activeTask?.title ?? t('dashboard.run.newTaskPlaceholder'),
          }),
        },
        {
          title: t('dashboard.run.startParamsTitle'),
          items: [
            t('dashboard.run.paramRealtime', { status: realtimeApi ? 'ON' : 'OFF' }),
            t('dashboard.run.paramTokens', { limit: tokensLimit }),
            t('dashboard.run.adjustAgentsHint'),
          ],
        },
      ],
    });

    const agentPayload = agents.map((agent) => ({
      id: agent.id,
      type: agent.type,
      model: agent.model,
      prompt: agent.prompt,
    }));

    const payload = {
      question: trimmedQuestion,
      context: '',
      options: [],
      criteria: [],
      agents: agentPayload,
    };

    if (activeTask) {
      payload.project_id = activeTask.projectId;
      payload.task_id = activeTask.id;
    } else {
      payload.project_name = generateProjectName(trimmedQuestion);
      payload.task_title = generateTaskTitle(trimmedQuestion);
    }

    try {
      const response = await runDecisionTask(payload);
      setActiveRun({ runId: response.run_id, taskId: response.task_id });
      setActiveTaskId(response.task_id);
      await refreshWorkspace(response.task_id);
    } catch (error) {
      console.error('Failed to start decision', error);
      window.alert(t('dashboard.run.failedTitle'));
      setIsRunning(false);
      setActiveRun(null);
    }
  };

  const handleClearInput = () => {
    setQuestion('');
  };

  useEffect(() => {
    if (!activeRun?.runId) {
      return undefined;
    }

    let cancelled = false;
    const startTime = Date.now();

    const pollStatus = async () => {
      try {
        const status = await fetchDecisionStatus(activeRun.runId);
        if (cancelled) {
          return;
        }

        setElapsed(formatDuration(Date.now() - startTime));

        const resolvedStage = resolveStageIndex(status.stage, stages);
        if (resolvedStage) {
          setCurrentStage(resolvedStage);
        }

        if (typeof status.error_count === 'number') {
          setErrors(status.error_count);
        }

        updateTaskProgress(activeRun.taskId, {
          stage: status.stage,
          progress: status.progress,
          last_run_status: status.status,
          updated_at: status.updated_at ?? new Date().toISOString(),
        });

        if (status.status === 'completed' || status.status === 'failed' || status.status === 'cancelled') {
          const result = await fetchDecisionResult(activeRun.runId);
          if (!cancelled) {
            setReport(buildSectionsFromResult(result, t, locale));
            setIsRunning(false);
            setActiveRun(null);
            await refreshWorkspace(activeRun.taskId);
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
  }, [activeRun, stages, t, locale, updateTaskProgress, refreshWorkspace]);

  return (
    <div className={styles.dashboard}>
      <div className={styles.sidebarArea}>
        <TaskSidebar
          projects={projects}
          activeTaskId={activeTaskId}
          onSelectTask={setActiveTaskId}
          onAddProject={isAuthenticated ? handleAddProject : null}
          onAddTask={isAuthenticated ? handleAddTask : null}
          onRenameProject={isAuthenticated ? handleRenameProject : null}
          onDeleteProject={isAuthenticated ? handleDeleteProject : null}
          onDeleteTask={isAuthenticated ? handleDeleteTask : null}
          isLoading={workspaceLoading}
          errorMessage={workspaceError}
        />
      </div>

      <div className={styles.mainArea}>
        <div className={styles.progressArea}>
          <StageProgress currentStage={currentStage} stages={stages} elapsed={elapsed} errors={errors} />
        </div>

        <div className={styles.controlsArea}>
          <div className={styles.agentsArea}>
            <AgentGrid
              agents={agents}
              onModelChange={handleModelChange}
              onPromptChange={handlePromptChange}
            />
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
            onExport={() => window.alert(t('dashboard.alert.exportPending'))}
            onCopy={() => window.alert(t('dashboard.alert.copyPending'))}
            onToggleTheme={() => window.alert(t('dashboard.alert.themePending'))}
          />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
