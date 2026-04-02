import PropTypes from 'prop-types';
import clsx from 'clsx';
import styles from './DecisionInput.module.css';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

function DecisionInput({
  value,
  onChange,
  onRun,
  onClear,
  realtimeApi,
  onToggleRealtimeApi,
  tokensLimit,
  onTokensLimitChange,
  isRunning,
}) {
  const { t } = useLanguage();

  return (
    <section className={`glass-panel ${styles.container}`}>
      <div>
        <div className={styles.label}>{t('decisionInput.label')}</div>
        <textarea
          className={styles.textarea}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder={t('decisionInput.placeholder')}
        />
      </div>

      <div className={styles.actions}>
        <button type="button" className={styles.button} onClick={onClear} disabled={!value.trim()}>
          {t('decisionInput.clear')}
        </button>
        <button
          type="button"
          className={clsx(styles.button, styles.buttonPrimary)}
          onClick={onRun}
          disabled={isRunning || !value.trim()}
        >
          {isRunning ? t('decisionInput.running') : t('decisionInput.run')}
        </button>
      </div>

      <div className={styles.controlsRow}>
        <label className={clsx(styles.switch, realtimeApi && styles.switchActive)}>
          <span className={styles.switchTrack}>
            <span className={styles.switchThumb} />
          </span>
          <input
            type="checkbox"
            checked={realtimeApi}
            onChange={(event) => onToggleRealtimeApi(event.target.checked)}
            hidden
          />
          {t('decisionInput.realtime')}
        </label>

        <div className={styles.sliderRow}>
          {t('decisionInput.tokensLimit')}
          <input
            type="range"
            min="512"
            max="4096"
            step="256"
            value={tokensLimit}
            onChange={(event) => onTokensLimitChange(Number(event.target.value))}
          />
          <span>{tokensLimit}</span>
        </div>
      </div>
    </section>
  );
}

DecisionInput.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  onRun: PropTypes.func.isRequired,
  onClear: PropTypes.func.isRequired,
  realtimeApi: PropTypes.bool.isRequired,
  onToggleRealtimeApi: PropTypes.func.isRequired,
  tokensLimit: PropTypes.number.isRequired,
  onTokensLimitChange: PropTypes.func.isRequired,
  isRunning: PropTypes.bool.isRequired,
};

export default DecisionInput;
