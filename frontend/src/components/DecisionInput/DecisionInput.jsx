import PropTypes from 'prop-types';
import clsx from 'clsx';
import styles from './DecisionInput.module.css';

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
  return (
    <section className={`glass-panel ${styles.container}`}>
      <div>
        <div className={styles.label}>输入决策问题</div>
        <textarea
          className={styles.textarea}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="描述需要协作分析的问题、背景与目标..."
        />
      </div>

      <div className={styles.actions}>
        <button type="button" className={styles.button} onClick={onClear} disabled={!value.trim()}>
          Clear
        </button>
        <button
          type="button"
          className={clsx(styles.button, styles.buttonPrimary)}
          onClick={onRun}
          disabled={isRunning || !value.trim()}
        >
          {isRunning ? '运行中...' : 'Run Decision'}
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
          实时 API
        </label>

        <div className={styles.sliderRow}>
          Tokens 限制
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
