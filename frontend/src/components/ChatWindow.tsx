import React, { useRef, useEffect } from 'react';
import { ChatMessage, DisplayMessage } from './ChatMessage';
import { SuggestionCard } from './SuggestionCard';
import { SupportedLanguage } from '../types/api';

interface ChatWindowProps {
  messages: DisplayMessage[];
  onSelectSuggestion: (suggestion: string) => void;
  onOpenEligibilityModal?: () => void;
  isLoading: boolean;
  language?: SupportedLanguage;
}

const CATEGORIES_TA = [
  {
    icon: '🎓',
    title: 'கல்வி',
    subtitle: 'மாணவர்களுக்கான திட்டங்கள்',
    query: 'மாணவர்களுக்கு என்ன அரசு திட்டங்கள் உள்ளன?',
  },
  {
    icon: '👩',
    title: 'பெண்கள்',
    subtitle: 'பெண்களுக்கான நலத்திட்டங்கள்',
    query: 'பெண்களுக்கான அரசு நலத்திட்டங்கள் என்ன?',
  },
  {
    icon: '💼',
    title: 'வேலைவாய்ப்பு',
    subtitle: 'வேலை மற்றும் திறன் மேம்பாடு',
    query: 'வேலைவாய்ப்பு மற்றும் திறன் மேம்பாட்டு திட்டங்கள் என்ன?',
  },
  {
    icon: '💰',
    title: 'நிதியுதவி',
    subtitle: 'நிதி மற்றும் சமூக பாதுகாப்பு',
    query: 'நிதி உதவி மற்றும் சமூக பாதுகாப்பு திட்டங்கள் என்னென்ன?',
  },
];

const CATEGORIES_EN = [
  {
    icon: '🎓',
    title: 'Education',
    subtitle: 'Schemes for students',
    query: 'What government schemes are available for students?',
  },
  {
    icon: '👩',
    title: 'Women',
    subtitle: 'Welfare schemes for women',
    query: 'What government welfare schemes are available for women?',
  },
  {
    icon: '💼',
    title: 'Employment',
    subtitle: 'Jobs & skill development',
    query: 'What employment and skill development schemes are available?',
  },
  {
    icon: '💰',
    title: 'Financial Assistance',
    subtitle: 'Financial & social security',
    query: 'What financial assistance and social security schemes are available?',
  },
];

const SUGGESTED_QUESTIONS_TA = [
  'மாணவர்களுக்கு என்ன அரசு திட்டங்கள் உள்ளன?',
  'பெண்களுக்கான அரசு நலத்திட்டங்கள் என்ன?',
  'எனக்கு என்ன அரசு உதவிகள் கிடைக்கும்?',
  'இந்த திட்டத்திற்கு நான் தகுதியானவரா?',
];

const SUGGESTED_QUESTIONS_EN = [
  'What government schemes are available for students?',
  'What government welfare schemes are available for women?',
  'What government assistance can I get?',
  'Am I eligible for this scheme?',
];

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  onSelectSuggestion,
  onOpenEligibilityModal,
  isLoading,
  language = 'ta',
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);
  const isEn = language === 'en';

  const categories = isEn ? CATEGORIES_EN : CATEGORIES_TA;
  const suggestedQuestions = isEn ? SUGGESTED_QUESTIONS_EN : SUGGESTED_QUESTIONS_TA;

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="chat-window-container" role="region" aria-label={isEn ? 'Chat Conversation Area' : 'உரையாடல் பகுதி'}>
      {messages.length === 0 ? (
        <div className="welcome-hero-fullwidth">
          <div className="hero-welcome-badge">
            <span className="wave-hand">{isEn ? 'Hello! 👋' : 'வணக்கம்! 👋'}</span>
          </div>

          <h2 className="hero-title">
            {isEn
              ? 'Find government welfare schemes relevant to you'
              : 'உங்களுக்கு தேவையான அரசு நலத்திட்டங்களை கண்டறியுங்கள்'}
          </h2>

          <p className="hero-description">
            {isEn
              ? 'NammaSahay AI helps you discover Tamil Nadu government welfare schemes based on your age, education, occupation, and family income.'
              : 'உங்கள் வயது, கல்வி, தொழில் மற்றும் வருமானம் போன்ற தகவல்களின் அடிப்படையில் உங்களுக்கு பொருந்தக்கூடிய அரசு நலத்திட்டங்களை கண்டறிய NammaSahay AI உதவுகிறது.'}
          </p>

          {onOpenEligibilityModal && (
            <div className="hero-cta-block">
              <button
                type="button"
                className="hero-primary-cta-btn"
                onClick={onOpenEligibilityModal}
              >
                {isEn ? '🎯 Check My Eligibility' : '🎯 எனது தகுதியை சரிபார்க்கவும்'}
              </button>
            </div>
          )}

          <div className="section-divider-heading">
            <h3>{isEn ? '📌 Welfare Scheme Categories' : '📌 நலத்திட்ட பிரிவுகள்'}</h3>
          </div>

          <div className="categories-grid-4col">
            {categories.map((cat, idx) => (
              <SuggestionCard
                key={idx}
                variant="category"
                icon={cat.icon}
                text={cat.title}
                subtitle={cat.subtitle}
                language={language}
                onClick={() => onSelectSuggestion(cat.query)}
              />
            ))}
          </div>

          <div className="section-divider-heading suggestions-label-heading">
            <h3>{isEn ? '💬 Suggested Questions' : '💬 பரிந்துரைக்கப்பட்ட கேள்விகள்'}</h3>
          </div>

          <div className="suggestions-grid">
            {suggestedQuestions.map((question, idx) => (
              <SuggestionCard
                key={idx}
                variant="chip"
                text={question}
                language={language}
                onClick={onSelectSuggestion}
              />
            ))}
          </div>
        </div>
      ) : (
        <div className="messages-list">
          {messages.map((m) => (
            <ChatMessage key={m.id} message={m} language={language} />
          ))}
          {isLoading && (
            <div className="loading-row" aria-live="polite">
              <div className="avatar assistant-avatar" aria-hidden="true">
                🏛️
              </div>
              <div className="loading-indicator">
                <span className="loading-spinner" aria-hidden="true">⏳</span>
                <span className="loading-text">
                  {isEn
                    ? 'Fetching welfare scheme information... Please wait'
                    : 'நலத்திட்ட தகவல்கள் பெறப்படுகின்றன... தயவுசெய்து காத்திருக்கவும்'}
                </span>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      )}
    </div>
  );
};
