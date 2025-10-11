import PropTypes from 'prop-types';
import clsx from 'clsx';
import styles from './StageProgress.module.css';

function StageProgress({ currentStage, stages, elapsed, errors }) {
  return (
    <section className={`glass-panel ${styles.progress}`}>
      <div className={styles.titleRow}>
        <h2 className={`${styles.title} neon-text`}>任务进度</h2>
        <div className={styles.metrics}>
          <div className={styles.metric}>
            已用时<strong>{elapsed}</strong>
          </div>
          <div className={styles.metric}>
            错误<strong>{errors}</strong>
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
              className={clsx(styles.segment, isCompleted && styles.segmentCompleted, isActive && styles.segmentActive)}
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
