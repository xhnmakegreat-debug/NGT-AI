import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import styles from './TaskSidebar.module.css';
import { useLanguage } from '../../i18n/LanguageContext.jsx';
import { useAuth } from '../../context/AuthContext.jsx';

function formatUpdatedAt(value) {
  if (!value) {
    return '';
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return '';
  }
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function TaskSidebar({
  projects,
  activeTaskId,
  onSelectTask,
  onAddProject,
  onAddTask,
  onRenameProject,
  onDeleteProject,
  onDeleteTask,
  isLoading,
  errorMessage,
}) {
  const { t } = useLanguage();
  const { user, isAuthenticated, logout } = useAuth();
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const userMenuRef = useRef(null);

  const userDisplayName = useMemo(() => {
    if (user?.nickname) return user.nickname;
    if (user?.email) return user.email.split('@')[0] ?? '';
    return '';
  }, [user]);

  const totalTasks = useMemo(
    () => projects.reduce((sum, project) => sum + (project.tasks?.length ?? 0), 0),
    [projects],
  );

  const toggleUserMenu = useCallback(() => {
    setUserMenuOpen((prev) => !prev);
  }, []);

  const handleLogout = useCallback(() => {
    setUserMenuOpen(false);
    logout();
  }, [logout]);

  useEffect(() => {
    if (!userMenuOpen) {
      return undefined;
    }

    const handleClickOutside = (event) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setUserMenuOpen(false);
      }
    };

    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        setUserMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [userMenuOpen]);

  useEffect(() => {
    if (!isAuthenticated && userMenuOpen) {
      setUserMenuOpen(false);
    }
  }, [isAuthenticated, userMenuOpen]);

  const handleRenameProject = useCallback(
    (project) => {
      if (!onRenameProject) return;
      onRenameProject(project.id, project.name);
    },
    [onRenameProject],
  );

  const handleDeleteProject = useCallback(
    (projectId) => {
      if (!onDeleteProject) return;
      onDeleteProject(projectId);
    },
    [onDeleteProject],
  );

  const handleAddTask = useCallback(
    (projectId) => {
      if (!onAddTask) return;
      onAddTask(projectId);
    },
    [onAddTask],
  );

  const handleDeleteTask = useCallback(
    (taskId) => {
      if (!onDeleteTask) return;
      onDeleteTask(taskId);
    },
    [onDeleteTask],
  );

  return (
    <aside className={`glass-panel ${styles.sidebar}`}>
      <div className={styles.header}>
        <div className={styles.headerMain}>
          <h2 className={styles.title}>{t('sidebar.title')}</h2>
          <button
            type="button"
            className={styles.addButton}
            onClick={onAddProject}
            aria-label={t('sidebar.addProject')}
            disabled={!onAddProject}
          >
            +
          </button>
        </div>
        {isAuthenticated && (
          <div ref={userMenuRef} className={styles.userMenu}>
            <button
              type="button"
              className={styles.userMenuButton}
              onClick={toggleUserMenu}
              aria-haspopup="menu"
              aria-expanded={userMenuOpen}
            >
              <span className={styles.userAvatar}>
                {userDisplayName ? userDisplayName.charAt(0).toUpperCase() : '?'}
              </span>
              <span className={styles.userName}>{userDisplayName || t('userMenu.anonymous')}</span>
            </button>
            {userMenuOpen && (
              <div role="menu" className={styles.userDropdown}>
                <button type="button" role="menuitem" onClick={handleLogout}>
                  {t('userMenu.logout') ?? 'Logout'}
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      <div className={`${styles.scrollArea} scrollbar-thin`}>
        <div className={styles.sectionCaption}>{t('sidebar.projects')}</div>

        {errorMessage && <div className={styles.errorBanner}>{errorMessage}</div>}

        {!isLoading && totalTasks === 0 && (
          <div className={styles.emptyState}>{t('sidebar.emptyProject')}</div>
        )}

        {projects.map((project) => (
          <div key={project.id} className={styles.projectCard}>
            <div className={styles.projectHeader}>
              <div className={styles.projectMeta}>
                <span className={styles.projectName}>{project.name}</span>
                {project.summary && <span className={styles.projectSummary}>{project.summary}</span>}
                {project.path && <span className={styles.projectPath}>{project.path}</span>}
              </div>
              <div className={styles.projectActions}>
                {onAddTask && (
                  <button
                    type="button"
                    className={styles.iconButton}
                    onClick={() => handleAddTask(project.id)}
                    aria-label={t('sidebar.addTask')}
                  >
                    +
                  </button>
                )}
                {onRenameProject && (
                  <button
                    type="button"
                    className={styles.iconButton}
                    onClick={() => handleRenameProject(project)}
                    aria-label={t('sidebar.renameProjectAria', { name: project.name })}
                  >
                    ✎
                  </button>
                )}
                {onDeleteProject && (
                  <button
                    type="button"
                    className={clsx(styles.iconButton, styles.dangerButton)}
                    onClick={() => handleDeleteProject(project.id)}
                    aria-label="Delete project"
                  >
                    ×
                  </button>
                )}
              </div>
            </div>

            {project.tasks?.length ? (
              <div className={styles.taskList}>
                {project.tasks.map((task) => {
                  const stageLabel = task.stage || t('sidebar.stageUnknown');
                  const progressLabel =
                    typeof task.progress === 'number' ? `${task.progress}%` : '—';
                  const updatedAt = formatUpdatedAt(task.updated_at);

                  return (
                    <div
                      key={task.id}
                      className={clsx(
                        styles.taskItem,
                        task.id === activeTaskId && styles.taskItemActive,
                      )}
                    >
                      <button
                        type="button"
                        className={styles.taskButton}
                        onClick={() => onSelectTask(task.id)}
                      >
                        <div className={styles.taskHeader}>
                          <span className={styles.taskTitle}>{task.title}</span>
                          {onDeleteTask && (
                            <button
                              type="button"
                              className={styles.taskDeleteButton}
                              onClick={(event) => {
                                event.stopPropagation();
                                handleDeleteTask(task.id);
                              }}
                              aria-label={t('sidebar.deleteTaskConfirm')}
                            >
                              ×
                            </button>
                          )}
                        </div>
                        <div className={styles.taskMeta}>
                          <span className={styles.taskStage}>{stageLabel}</span>
                          <span className={styles.taskProgress}>{progressLabel}</span>
                        </div>
                        {updatedAt && (
                          <div className={styles.taskTimestamp}>{updatedAt}</div>
                        )}
                      </button>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className={styles.emptyProject}>{t('sidebar.emptyProject')}</div>
            )}
          </div>
        ))}
      </div>

      <div className={styles.footer}>
        <div className={styles.statusRow}>
          <div className={styles.statusIndicator}>
            <span className={styles.statusDot} />
            {t('sidebar.systemOnline')}
          </div>
          <span>{t('sidebar.taskCount', { count: totalTasks })}</span>
        </div>
      </div>
    </aside>
  );
}

TaskSidebar.propTypes = {
  projects: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      summary: PropTypes.string,
      path: PropTypes.string,
      tasks: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.string.isRequired,
          title: PropTypes.string.isRequired,
          stage: PropTypes.string,
          progress: PropTypes.number,
          updated_at: PropTypes.string,
        }),
      ),
    }),
  ).isRequired,
  activeTaskId: PropTypes.string,
  onSelectTask: PropTypes.func.isRequired,
  onAddProject: PropTypes.func,
  onAddTask: PropTypes.func,
  onRenameProject: PropTypes.func,
  onDeleteProject: PropTypes.func,
  onDeleteTask: PropTypes.func,
  isLoading: PropTypes.bool,
  errorMessage: PropTypes.string,
};

TaskSidebar.defaultProps = {
  activeTaskId: null,
  onAddProject: undefined,
  onAddTask: undefined,
  onRenameProject: undefined,
  onDeleteProject: undefined,
  onDeleteTask: undefined,
  isLoading: false,
  errorMessage: null,
};

export default TaskSidebar;
