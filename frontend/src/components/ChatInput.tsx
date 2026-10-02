import React, { useState } from 'react';
import { Send } from 'lucide-react';
import { SupportedLanguage } from '../types/api';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  language?: SupportedLanguage;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading, language = 'ta' }) => {
  const [text, setText] = useState('');
  const isEn = language === 'en';

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (text.trim() && !isLoading) {
      onSendMessage(text.trim());
      setText('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form className="chat-input-container" onSubmit={handleSubmit} role="search">
      <textarea
        className="chat-textarea"
        placeholder={isEn ? 'Type your query here in Tamil or English...' : 'உங்கள் கேள்வியை தமிழில் எழுதுங்கள்...'}
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isLoading}
        rows={1}
        aria-label={isEn ? 'Query input field' : 'கேள்வி பதிவு பெட்டி'}
      />
      <button
        type="submit"
        className="send-button"
        disabled={!text.trim() || isLoading}
        aria-label={isEn ? 'Send message' : 'கேள்வியை அனுப்பு'}
      >
        <Send size={22} />
        <span>{isEn ? 'Send' : 'அனுப்பு'}</span>
      </button>
    </form>
  );
};
