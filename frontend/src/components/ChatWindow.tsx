import React, { useRef, useEffect } from 'react';
import { ChatMessage, DisplayMessage } from './ChatMessage';
import { SuggestionCard } from './SuggestionCard';

interface ChatWindowProps {
  messages: DisplayMessage[];
  onSelectSuggestion: (suggestion: string) => void;
  onOpenEligibilityModal?: () => void;
  isLoading: boolean;
}

const CATEGORIES = [
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

const SUGGESTED_QUESTIONS = [
  'மாணவர்களுக்கு என்ன அரசு திட்டங்கள் உள்ளன?',
  'பெண்களுக்கான அரசு நலத்திட்டங்கள் என்ன?',
  'எனக்கு என்ன அரசு உதவிகள் கிடைக்கும்?',
  'இந்த திட்டத்திற்கு நான் தகுதியானவரா?',
];

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  onSelectSuggestion,
  onOpenEligibilityModal,
  isLoading,
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="chat-window-container" role="region" aria-label="உரையாடல் பகுதி">
      {messages.length === 0 ? (
        <div className="welcome-hero-fullwidth">
          <div className="hero-welcome-badge">
            <span className="wave-hand">வணக்கம்! 👋</span>
          </div>

          <h2 className="hero-title">
            உங்களுக்கு தேவையான அரசு நலத்திட்டங்களை கண்டறியுங்கள்
          </h2>

          <p className="hero-description">
            உங்கள் வயது, கல்வி, தொழில் மற்றும் வருமானம் போன்ற தகவல்களின் அடிப்படையில் உங்களுக்கு பொருந்தக்கூடிய அரசு நலத்திட்டங்களை கண்டறிய NammaSahay AI உதவுகிறது.
          </p>

          {onOpenEligibilityModal && (
            <div className="hero-cta-block">
              <button
                type="button"
                className="hero-primary-cta-btn"
                onClick={onOpenEligibilityModal}
              >
                🎯 எனது தகுதியை சரிபார்க்கவும்
              </button>
            </div>
          )}

          <div className="section-divider-heading">
            <h3>📌 நலத்திட்ட பிரிவுகள்</h3>
          </div>

          <div className="categories-grid-4col">
            {CATEGORIES.map((cat, idx) => (
              <SuggestionCard
                key={idx}
                variant="category"
                icon={cat.icon}
                text={cat.title}
                subtitle={cat.subtitle}
                onClick={() => onSelectSuggestion(cat.query)}
              />
            ))}
          </div>

          <div className="section-divider-heading suggestions-label-heading">
            <h3>💬 பரிந்துரைக்கப்பட்ட கேள்விகள்</h3>
          </div>

          <div className="suggestions-grid">
            {SUGGESTED_QUESTIONS.map((question, idx) => (
              <SuggestionCard
                key={idx}
                variant="chip"
                text={question}
                onClick={onSelectSuggestion}
              />
            ))}
          </div>
        </div>
      ) : (
        <div className="messages-list">
          {messages.map((m) => (
            <ChatMessage key={m.id} message={m} />
          ))}
          {isLoading && (
            <div className="loading-row" aria-live="polite">
              <div className="avatar assistant-avatar" aria-hidden="true">
                🏛️
              </div>
              <div className="loading-indicator">
                <span className="loading-spinner" aria-hidden="true">⏳</span>
                <span className="loading-text">
                  நலத்திட்ட தகவல்கள் பெறப்படுகின்றன... தயவுசெய்து காத்திருக்கவும்
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
