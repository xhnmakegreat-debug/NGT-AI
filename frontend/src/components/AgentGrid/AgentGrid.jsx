import PropTypes from 'prop-types';
import AgentCard from '../AgentCard/AgentCard.jsx';
import styles from './AgentGrid.module.css';

function AgentGrid({ agents, onModelChange, onPromptChange }) {
  return (
    <section className={`glass-panel ${styles.wrapper}`}>
      <div className={styles.titleRow}>
        <h2 className={`${styles.title} neon-text`}>多智能体配置</h2>
        <div className={styles.legend}>
          <span className={styles.legendItem}>
            <span className={styles.legendSwatch} />
            讨论员
          </span>
          <span className={styles.legendItem}>
            <span className={`${styles.legendSwatch} ${styles.legendSwatchReferee}`} />
            裁判
          </span>
        </div>
      </div>
      <div className={`${styles.grid} scrollbar-thin`}>
        {agents.map((agent) => (
          <AgentCard
            key={agent.id}
            agent={agent}
            onModelChange={onModelChange}
            onPromptChange={onPromptChange}
          />
        ))}
      </div>
    </section>
  );
}

AgentGrid.propTypes = {
  agents: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      type: PropTypes.oneOf(['discussant', 'referee']).isRequired,
      model: PropTypes.string.isRequired,
      prompt: PropTypes.string.isRequired,
      averageScore: PropTypes.number.isRequired,
      scoreHistory: PropTypes.arrayOf(PropTypes.number).isRequired,
    }),
  ).isRequired,
  onModelChange: PropTypes.func.isRequired,
  onPromptChange: PropTypes.func.isRequired,
};

export default AgentGrid;
