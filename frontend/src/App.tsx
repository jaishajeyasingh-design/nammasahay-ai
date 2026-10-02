import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { ChatWindow } from './components/ChatWindow';
import { ChatInput } from './components/ChatInput';
import { Footer } from './components/Footer';
import { DisplayMessage } from './components/ChatMessage';
import { EligibilityModal } from './components/EligibilityModal';
import { sendChatQuery } from './services/api';
import { SupportedLanguage, UserProfile } from './types/api';

export type FontScale = 'normal' | 'large' | 'xlarge';

export function App() {
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState<SupportedLanguage>('ta');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [fontScale, setFontScale] = useState<FontScale>(() => {
    return (localStorage.getItem('nammasahay_font_scale') as FontScale) || 'normal';
  });

  useEffect(() => {
    document.documentElement.className = `font-scale-${fontScale}`;
  }, [fontScale]);

  const handleFontScaleChange = (scale: FontScale) => {
    setFontScale(scale);
    localStorage.setItem('nammasahay_font_scale', scale);
  };

  const handleSendMessage = async (queryText: string, profile?: UserProfile) => {
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Add user message to UI
    const userMsgText = profile
      ? `🎯 சுயவிவர தகுதி சரிபார்ப்பு`
      : queryText;

    const userMsg: DisplayMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: userMsgText,
      timestamp,
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      // Call existing backend API service with user_profile
      const response = await sendChatQuery({
        message: queryText,
        language: language,
        user_profile: profile,
      });

      const assistantMsg: DisplayMessage = {
        id: `assistant-${Date.now()}`,
        sender: 'assistant',
        text: language === 'en' ? (response.response_english || response.response_tamil) : (response.response_tamil || response.response_english),
        responseObject: response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (error) {
      console.error('Error fetching chat response:', error);

      const errorMsg: DisplayMessage = {
        id: `error-${Date.now()}`,
        sender: 'assistant',
        text: 'மன்னிக்கவும்! தற்போது சேவையை அணுக முடியவில்லை.\nBackend server இயங்குகிறதா என்பதை சரிபார்க்கவும்.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleProfileSubmit = (profile: UserProfile) => {
    handleSendMessage('எனக்கான அரசு நலத்திட்டங்கள் மற்றும் தகுதி விவரங்கள் என்ன?', profile);
  };

  return (
    <div className={`app-container font-scale-${fontScale}`}>
      <Header
        currentLanguage={language}
        onLanguageToggle={(newLang) => setLanguage(newLang)}
        onOpenEligibilityModal={() => setIsModalOpen(true)}
        fontScale={fontScale}
        onFontScaleChange={handleFontScaleChange}
      />
      <main className="main-content">
        <ChatWindow
          messages={messages}
          onSelectSuggestion={(query) => handleSendMessage(query)}
          onOpenEligibilityModal={() => setIsModalOpen(true)}
          isLoading={isLoading}
        />
        <ChatInput onSendMessage={(query) => handleSendMessage(query)} isLoading={isLoading} />
      </main>
      <Footer />

      <EligibilityModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmitProfile={handleProfileSubmit}
        isLoading={isLoading}
      />
    </div>
  );
}

export default App;
