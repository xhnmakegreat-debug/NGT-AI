import PropTypes from 'prop-types';
import styles from './ReportViewer.module.css';

function ReportViewer({ report, onExport, onCopy, onToggleTheme }) {
  const hasSections = Array.isArray(report.sections) && report.sections.length > 0;

  return (
    <section className={`glass-panel ${styles.container}`}>
      <header className={styles.toolbar}>
        <h2 className={`${styles.toolbarTitle} neon-text`}>协作报告</h2>
        <div className={styles.actions}>
          <button type="button" className={styles.actionButton} onClick={onExport}>
            导出
          </button>
          <button type="button" className={styles.actionButton} onClick={onCopy}>
            复制
          </button>
          <button type="button" className={styles.actionButton} onClick={onToggleTheme}>
            主题
          </button>
        </div>
      </header>

      <div className={`${styles.content} scrollbar-thin`}>
        {hasSections ? (
          report.sections.map((section) => (
            <div key={section.title} className={styles.section}>
              <h3>{section.title}</h3>
              {section.content && <p>{section.content}</p>}
              {Array.isArray(section.items) && section.items.length > 0 && (
                <ul className={styles.bulletList}>
                  {section.items.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              )}
            </div>
          ))
        ) : (
          <div className={styles.emptyState}>
            <div className={styles.emptyIllustration}>等待新的输出</div>
            <div>
              <strong>尚未生成任何报告</strong>
              <p>运行一次决策任务后，这里会展示完整的协作结果。</p>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

ReportViewer.propTypes = {
  report: PropTypes.shape({
    sections: PropTypes.arrayOf(
      PropTypes.shape({
        title: PropTypes.string.isRequired,
        content: PropTypes.string,
        items: PropTypes.arrayOf(PropTypes.string),
      }),
    ),
  }).isRequired,
  onExport: PropTypes.func.isRequired,
  onCopy: PropTypes.func.isRequired,
  onToggleTheme: PropTypes.func.isRequired,
};

export default ReportViewer;
