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
  
  // Restore language from localStorage 'nammasahay-language' with 'ta' default
  const [language, setLanguage] = useState<SupportedLanguage>(() => {
    return (localStorage.getItem('nammasahay-language') as SupportedLanguage) || 'ta';
  });

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

  const handleLanguageToggle = (newLang: SupportedLanguage) => {
    setLanguage(newLang);
    localStorage.setItem('nammasahay-language', newLang);
  };

  const handleSendMessage = async (queryText: string, profile?: UserProfile) => {
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Add user message to UI
    const userMsgText = profile
      ? (language === 'en' ? '🎯 Profile Eligibility Check' : '🎯 சுயவிவர தகுதி சரிபார்ப்பு')
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
      // Call backend API service with current selected language
      const response = await sendChatQuery({
        message: queryText,
        language: language,
        user_profile: profile,
      });

      const responseText = language === 'en'
        ? (response.response_english || response.response_tamil)
        : (response.response_tamil || response.response_english);

      const assistantMsg: DisplayMessage = {
        id: `assistant-${Date.now()}`,
        sender: 'assistant',
        text: responseText,
        responseObject: response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (error) {
      console.error('Error fetching chat response:', error);

      const errorMsgText = language === 'en'
        ? 'Sorry! Unable to connect to the service currently. Please check if the backend server is running.'
        : 'மன்னிக்கவும்! தற்போது சேவையை அணுக முடியவில்லை.\nBackend server இயங்குகிறதா என்பதை சரிபார்க்கவும்.';

      const errorMsg: DisplayMessage = {
        id: `error-${Date.now()}`,
        sender: 'assistant',
        text: errorMsgText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleProfileSubmit = (profile: UserProfile) => {
    const query = language === 'en'
      ? 'What government schemes and eligibility details are available for me?'
      : 'எனக்கான அரசு நலத்திட்டங்கள் மற்றும் தகுதி விவரங்கள் என்ன?';

    handleSendMessage(query, profile);
  };

  return (
    <div className={`app-container font-scale-${fontScale}`}>
      <Header
        currentLanguage={language}
        onLanguageToggle={handleLanguageToggle}
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
          language={language}
        />
        <ChatInput
          onSendMessage={(query) => handleSendMessage(query)}
          isLoading={isLoading}
          language={language}
        />
      </main>
      <Footer language={language} />

      <EligibilityModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmitProfile={handleProfileSubmit}
        isLoading={isLoading}
        language={language}
      />
    </div>
  );
}

export default App;
