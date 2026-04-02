import { useMemo } from 'react';
import PropTypes from 'prop-types';
import styles from './ReportViewer.module.css';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

function ReportViewer({ report, onExport, onCopy, onToggleTheme }) {
  const { t } = useLanguage();
  const displaySections = useMemo(() => {
    const sections = Array.isArray(report?.sections) ? report.sections : [];
    return sections.filter((section) => {
      if (!section) return false;
      if (section.hidden === true) return false;
      if (typeof section.type === 'string' && section.type.toLowerCase() === 'parameters') {
        return false;
      }
      const title = typeof section.title === 'string' ? section.title : '';
      if (!title) return true;
      const lowerTitle = title.toLowerCase();
      if (lowerTitle.includes('参数')) {
        return false;
      }
      if (lowerTitle.includes('parameter')) {
        return false;
      }
      return true;
    });
  }, [report]);
  const hasSections = displaySections.length > 0;

  return (
    <section className={`glass-panel ${styles.container}`}>
      <header className={styles.toolbar}>
        <h2 className={`${styles.toolbarTitle} neon-text`}>{t('reportViewer.title')}</h2>
        <div className={styles.actions}>
          <button type="button" className={styles.actionButton} onClick={onExport}>
            {t('reportViewer.export')}
          </button>
          <button type="button" className={styles.actionButton} onClick={onCopy}>
            {t('reportViewer.copy')}
          </button>
          <button type="button" className={styles.actionButton} onClick={onToggleTheme}>
            {t('reportViewer.theme')}
          </button>
        </div>
      </header>

      <div className={`${styles.content} scrollbar-thin`}>
        {hasSections ? (
          displaySections.map((section) => (
            <div key={section.title} className={styles.section}>
              <h3>{section.title}</h3>
              {section.content && <p>{section.content}</p>}
              {Array.isArray(section.items) && section.items.length > 0 && (
                <ul className={styles.bulletList}>
                  {section.items.map((item, index) => (
                    // eslint-disable-next-line react/no-array-index-key
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              )}
            </div>
          ))
        ) : (
          <div className={styles.emptyState}>
            <div className={styles.emptyIllustration}>{t('reportViewer.waiting')}</div>
            <div>
              <strong>{t('reportViewer.emptyTitle')}</strong>
              <p>{t('reportViewer.emptyHint')}</p>
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
