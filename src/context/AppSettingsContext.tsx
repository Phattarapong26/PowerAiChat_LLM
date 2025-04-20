
import React, { createContext, useState, useContext } from 'react';

type AIStyle = "formal" | "casual" | "friendly" | "professional";
type Language = "thai" | "english";

interface AppSettingsContextType {
  aiStyle: AIStyle;
  language: Language;
  setAiStyle: (style: AIStyle) => void;
  setLanguage: (language: Language) => void;
}

const AppSettingsContext = createContext<AppSettingsContextType>({
  aiStyle: "formal",
  language: "thai",
  setAiStyle: () => {},
  setLanguage: () => {},
});

export const AppSettingsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [aiStyle, setAiStyle] = useState<AIStyle>("formal");
  const [language, setLanguage] = useState<Language>("thai");

  return (
    <AppSettingsContext.Provider value={{ aiStyle, language, setAiStyle, setLanguage }}>
      {children}
    </AppSettingsContext.Provider>
  );
};

export const useAppSettings = () => useContext(AppSettingsContext);
