import PropTypes from 'prop-types';
import clsx from 'clsx';
import styles from './StageProgress.module.css';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

function StageProgress({ currentStage, stages, elapsed, errors }) {
  const { t, language, setLanguage, availableLanguages } = useLanguage();

  return (
    <section className={`glass-panel ${styles.progress}`}>
      <div className={styles.titleRow}>
        <h2 className={`${styles.title} neon-text`}>{t('stageProgress.title')}</h2>
        <div className={styles.metrics}>
          <div className={styles.metric}>
            {t('stageProgress.elapsed')}
            <strong>{elapsed}</strong>
          </div>
          <div className={styles.metric}>
            {t('stageProgress.errors')}
            <strong>{errors}</strong>
          </div>
          <div className={styles.languageSelector}>
            <label className={styles.languageLabel} htmlFor="language-select">
              {t('stageProgress.language')}
            </label>
            <select
              id="language-select"
              className={styles.languageSelect}
              value={language}
              onChange={(event) => setLanguage(event.target.value)}
            >
              {availableLanguages.map((option) => (
                <option key={option.code} value={option.code}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
      <div className={styles.capsule}>
        {stages.map((stage, index) => {
          const stageNumber = index + 1;
          const isCompleted = stageNumber < currentStage;
          const isActive = stageNumber === currentStage;
          return (
            <div
              key={stage}
              className={clsx(
                styles.segment,
                isCompleted && styles.segmentCompleted,
                isActive && styles.segmentActive,
              )}
            >
              {stageNumber}. {stage}
            </div>
          );
        })}
      </div>
    </section>
  );
}

StageProgress.propTypes = {
  currentStage: PropTypes.number.isRequired,
  stages: PropTypes.arrayOf(PropTypes.string).isRequired,
  elapsed: PropTypes.string.isRequired,
  errors: PropTypes.number.isRequired,
};

export default StageProgress;
