import { useState } from 'react';
import PropTypes from 'prop-types';

import styles from './LoginPanel.module.css';
import { useAuth } from '../../context/AuthContext.jsx';
import { useLanguage } from '../../i18n/LanguageContext.jsx';

function LoginPanel({ onAuthenticated = () => {} }) {
  const { t } = useLanguage();
  const { login, register } = useAuth();

  const [mode, setMode] = useState('login');
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [nickname, setNickname] = useState('');
  const [isSubmitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const toggleMode = () => {
    setMode((prev) => (prev === 'login' ? 'register' : 'login'));
    setError('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setError('');
    const trimmedIdentifier = identifier.trim();
    if (!trimmedIdentifier) {
      setError(t('auth.login.identifierRequired'));
      setSubmitting(false);
      return;
    }

    try {
      if (mode === 'login') {
        await login({ email: trimmedIdentifier, password });
      } else {
        const trimmedNickname = nickname.trim();
        await register({
          email: trimmedIdentifier,
          password,
          nickname: trimmedNickname || null,
        });
      }
      onAuthenticated();
    } catch (err) {
      setError(err?.message ?? t('auth.login.error'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.backdrop}>
      <div className={styles.shell}>
        <section className={styles.hero}>
          <div>
            <span className={styles.heroBadge}>{t('auth.hero.badge')}</span>
            <h2>{t('auth.hero.title')}</h2>
            <p>{t('auth.hero.subtitle')}</p>
          </div>
          <ul className={styles.heroList}>
            <li>{t('auth.hero.point1')}</li>
            <li>{t('auth.hero.point2')}</li>
            <li>{t('auth.hero.point3')}</li>
          </ul>
          <div className={styles.heroFooter}>{t('auth.hero.footer')}</div>
        </section>

        <section className={styles.formSection}>
          <header className={styles.header}>
            <div>
              <h1>{t('auth.login.title')}</h1>
              <p>{t('auth.login.subtitle')}</p>
            </div>
            <button type="button" className={styles.switch} onClick={toggleMode} disabled={isSubmitting}>
              {t(mode === 'login' ? 'auth.login.switchToRegister' : 'auth.login.switchToLogin')}
            </button>
          </header>

          <form className={styles.form} onSubmit={handleSubmit}>
            {mode === 'register' && (
              <label className={styles.field}>
                <span>{t('auth.login.nickname')}</span>
                <input
                  type="text"
                  value={nickname}
                  onChange={(event) => setNickname(event.target.value)}
                  placeholder={t('auth.login.nicknamePlaceholder')}
                />
              </label>
            )}

            <label className={styles.field}>
              <span>{t('auth.login.identifier')}</span>
              <input
                type="text"
                value={identifier}
                onChange={(event) => setIdentifier(event.target.value)}
                placeholder={t('auth.login.identifierPlaceholder')}
              />
            </label>

            <label className={styles.field}>
              <span>{t('auth.login.password')}</span>
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="••••••••"
                required
                minLength={8}
              />
            </label>

            {error && <div className={styles.error}>{error}</div>}

            <button type="submit" className={styles.submit} disabled={isSubmitting}>
              {isSubmitting
                ? t('auth.login.submitting')
                : t(mode === 'login' ? 'auth.login.submit' : 'auth.login.register')}
            </button>
          </form>

          <p className={styles.hint}>{t('auth.login.altHint')}</p>
        </section>
      </div>
    </div>
  );
}

LoginPanel.propTypes = {
  onAuthenticated: PropTypes.func,
};

export default LoginPanel;
