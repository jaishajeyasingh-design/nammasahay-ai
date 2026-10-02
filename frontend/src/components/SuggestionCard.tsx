import React from 'react';

interface SuggestionCardProps {
  text: string;
  subtitle?: string;
  icon?: string;
  onClick: (suggestion: string) => void;
  variant?: 'category' | 'chip';
}

export const SuggestionCard: React.FC<SuggestionCardProps> = ({
  text,
  subtitle,
  icon,
  onClick,
  variant = 'chip',
}) => {
  if (variant === 'category') {
    return (
      <button
        type="button"
        className="category-card"
        onClick={() => onClick(subtitle ? `${text} - ${subtitle}` : text)}
        aria-label={`${text}: ${subtitle || ''}`}
      >
        <div className="category-card-top">
          <span className="category-emoji" aria-hidden="true">{icon}</span>
          <h3 className="category-title">{text}</h3>
        </div>
        {subtitle && <p className="category-subtitle">{subtitle}</p>}
        <div className="category-action" aria-hidden="true">
          <span>திட்டங்களைப் பார்க்கவும்</span>
          <span className="action-arrow">→</span>
        </div>
      </button>
    );
  }

  return (
    <button
      type="button"
      className="suggestion-chip"
      onClick={() => onClick(text)}
      aria-label={text}
    >
      <span className="suggestion-chip-text">{text}</span>
      <span className="suggestion-chip-icon" aria-hidden="true">→</span>
    </button>
  );
};
