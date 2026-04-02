import PropTypes from 'prop-types';
import clsx from 'clsx';
import styles from './AgentCard.module.css';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

const MODEL_OPTIONS = [
  { value: 'gpt-4o', label: 'GPT-4' },
  { value: 'claude-3-opus', label: 'Claude' },
  { value: 'gemini-1.5-pro', label: 'Gemini' },
  { value: 'qwen-long', label: 'Qwen' },
  { value: 'deepseek-chat', label: 'DeepSeek' },
  { value: 'grok-beta', label: 'Grok' },
];

function AgentCard({ agent, onModelChange, onPromptChange }) {
  const isReferee = agent.type === 'referee';
  const { t } = useLanguage();

  return (
    <article className={clsx('glass-panel', styles.card, isReferee && styles.cardReferee)}>
      <div className={styles.header}>
        <div className={clsx(styles.avatar, isReferee && styles.refereeAvatar)}>{agent.id}</div>
        <select
          className={styles.modelSelect}
          value={agent.model}
          onChange={(event) => onModelChange(agent.id, event.target.value)}
        >
          {MODEL_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <span className={styles.promptLabel}>{t('agentCard.promptLabel')}</span>
        <textarea
          className={styles.promptInput}
          value={agent.prompt}
          onChange={(event) => onPromptChange(agent.id, event.target.value)}
          rows={3}
        />
      </div>

      <div className={styles.stats}>
        <div className={styles.score}>
          <span>{t('agentCard.averageScore')}</span>
          <strong>{agent.averageScore.toFixed(1)}</strong>
        </div>
        <div className={styles.sparkline}>
          {agent.scoreHistory.map((score, index) => (
            <span
              // eslint-disable-next-line react/no-array-index-key
              key={index}
              className={clsx(
                styles.sparklineBar,
                score < agent.averageScore && styles.sparklineBarMuted,
              )}
              style={{ height: `${Math.max(score / 5, 0.1) * 100}%` }}
            />
          ))}
        </div>
      </div>
    </article>
  );
}

AgentCard.propTypes = {
  agent: PropTypes.shape({
    id: PropTypes.string.isRequired,
    type: PropTypes.oneOf(['discussant', 'referee']).isRequired,
    model: PropTypes.string.isRequired,
    prompt: PropTypes.string.isRequired,
    averageScore: PropTypes.number.isRequired,
    scoreHistory: PropTypes.arrayOf(PropTypes.number).isRequired,
  }).isRequired,
  onModelChange: PropTypes.func.isRequired,
  onPromptChange: PropTypes.func.isRequired,
};

export default AgentCard;
