import { createContext, useCallback, useContext, useMemo, useState } from 'react';
import PropTypes from 'prop-types';
import { SUPPORTED_LANGUAGES, translations, getLocaleFromLanguage } from './translations.js';

const LanguageContext = createContext({
  language: 'zh',
  setLanguage: () => {},
  availableLanguages: SUPPORTED_LANGUAGES,
  t: (key) => key,
  locale: 'zh-CN',
});

function formatTemplate(template, params) {
  if (!params) {
    return template;
  }
  return template.replace(/\{(\w+)\}/g, (match, token) => {
    if (Object.prototype.hasOwnProperty.call(params, token)) {
      const value = params[token];
      return value === undefined || value === null ? '' : String(value);
    }
    return match;
  });
}

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('zh');

  const translate = useCallback(
    (key, params) => {
      const langTable = translations[language] || translations.zh;
      const template = langTable[key];
      if (template === undefined) {
        const fallback = translations.zh?.[key];
        return formatTemplate(fallback ?? key, params);
      }
      return formatTemplate(template, params);
    },
    [language],
  );

  const value = useMemo(
    () => ({
      language,
      setLanguage,
      availableLanguages: SUPPORTED_LANGUAGES,
      t: translate,
      locale: getLocaleFromLanguage(language),
    }),
    [language, translate],
  );

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

LanguageProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export function useLanguage() {
  return useContext(LanguageContext);
}
