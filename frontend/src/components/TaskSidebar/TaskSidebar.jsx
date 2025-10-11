import { useMemo } from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import styles from './TaskSidebar.module.css';

function TaskSidebar({
  tasks,
  projects,
  activeTaskId,
  onSelectTask,
  onAddTask,
  filters,
  onToggleFilter,
  onRenameProject,
}) {
  const projectLookup = useMemo(() => {
    const map = new Map();
    projects.forEach((project) => map.set(project.id, project));
    return map;
  }, [projects]);

  const groupedProjects = useMemo(
    () =>
      projects.map((project) => ({
        ...project,
        tasks: tasks.filter((task) => task.projectId === project.id),
      })),
    [projects, tasks],
  );

  const orphanTasks = useMemo(
    () => tasks.filter((task) => !projectLookup.has(task.projectId)),
    [tasks, projectLookup],
  );

  const handleRename = (project) => {
    if (!onRenameProject) return;
    const nextName = window.prompt('重命名项目', project.name);
    if (nextName && nextName.trim() && nextName.trim() !== project.name) {
      onRenameProject(project.id, nextName.trim());
    }
  };

  return (
    <aside className={`glass-panel ${styles.sidebar}`}>
      <div className={styles.header}>
        <h2 className={styles.title}>决策任务</h2>
        <button type="button" className={styles.addButton} onClick={onAddTask} aria-label="添加任务">
          +
        </button>
      </div>

      <div className={`${styles.scrollArea} scrollbar-thin`}>
        <div className={styles.sectionCaption}>项目</div>
        {groupedProjects.map((project) => (
          <div key={project.id} className={styles.projectCard}>
            <div className={styles.projectHeader}>
              <div className={styles.projectMeta}>
                <span className={styles.projectName}>{project.name}</span>
                {project.summary && <span className={styles.projectSummary}>{project.summary}</span>}
                <span className={styles.projectPath}>{project.path}</span>
              </div>
              {onRenameProject ? (
                <button
                  type="button"
                  className={styles.renameButton}
                  onClick={() => handleRename(project)}
                  aria-label={`重命名 ${project.name}`}
                >
                  ✏️
                </button>
              ) : null}
            </div>
            {project.tasks.length > 0 ? (
              <div className={styles.taskList}>
                {project.tasks.map((task) => (
                  <button
                    key={task.id}
                    type="button"
                    className={clsx(styles.taskItem, task.id === activeTaskId && styles.taskItemActive)}
                    onClick={() => onSelectTask(task.id)}
                  >
                    <span className={styles.taskTitle}>{task.title}</span>
                    <span className={styles.taskMeta}>
                      <span>{task.stageLabel}</span>
                      <span>{task.updatedAt}</span>
                    </span>
                  </button>
                ))}
              </div>
            ) : (
              <div className={styles.emptyProject}>暂无任务，点击右上角添加或在运行后生成。</div>
            )}
          </div>
        ))}

        {orphanTasks.length > 0 && (
          <>
            <div className={styles.sectionCaption}>未归档任务</div>
            <div className={styles.taskList}>
              {orphanTasks.map((task) => (
                <button
                  key={task.id}
                  type="button"
                  className={clsx(styles.taskItem, task.id === activeTaskId && styles.taskItemActive)}
                  onClick={() => onSelectTask(task.id)}
                >
                  <span className={styles.taskTitle}>{task.title}</span>
                  <span className={styles.taskMeta}>
                    <span>{task.stageLabel}</span>
                    <span>{task.updatedAt}</span>
                  </span>
                </button>
              ))}
            </div>
          </>
        )}
      </div>

      <div className={styles.footer}>
        <div className={styles.tags}>
          {filters.map((filter) => (
            <button
              key={filter.id}
              type="button"
              className={clsx(styles.tag, filter.active && styles.tagActive)}
              onClick={() => onToggleFilter(filter.id)}
            >
              {filter.label}
            </button>
          ))}
        </div>
        <div className={styles.statusRow}>
          <div className={styles.statusIndicator}>
            <span className={styles.statusDot} />
            系统在线
          </div>
          <span>任务数：{tasks.length}</span>
        </div>
      </div>
    </aside>
  );
}

TaskSidebar.propTypes = {
  tasks: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      projectId: PropTypes.string.isRequired,
      stageLabel: PropTypes.string.isRequired,
      updatedAt: PropTypes.string.isRequired,
    }),
  ).isRequired,
  projects: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      path: PropTypes.string.isRequired,
      summary: PropTypes.string,
    }),
  ).isRequired,
  activeTaskId: PropTypes.string.isRequired,
  onSelectTask: PropTypes.func.isRequired,
  onAddTask: PropTypes.func.isRequired,
  filters: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
      active: PropTypes.bool.isRequired,
    }),
  ).isRequired,
  onToggleFilter: PropTypes.func.isRequired,
  onRenameProject: PropTypes.func,
};

TaskSidebar.defaultProps = {
  onRenameProject: undefined,
};

export default TaskSidebar;
