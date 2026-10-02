import React from 'react';
import { SupportedLanguage } from '../types/api';

interface FooterProps {
  language?: SupportedLanguage;
}

export const Footer: React.FC<FooterProps> = ({ language = 'ta' }) => {
  const isEn = language === 'en';

  return (
    <footer className="footer-container" role="contentinfo">
      <div className="footer-content">
        <p className="footer-trust">
          {isEn
            ? '🔒 NammaSahay AI • Tamil Nadu Government Scheme Assistant'
            : '🔒 NammaSahay AI • தமிழ்நாடு அரசு நலத்திட்ட வழிகாட்டி'}
        </p>
        <p className="footer-disclaimer">
          {isEn
            ? 'Information provided for guidance. Please verify details with official government portals before applying.'
            : 'தகவல்கள் வழிகாட்டலுக்கு மட்டுமே. விண்ணப்பிக்கும் முன் அதிகாரப்பூர்வ அரசு அறிவிப்புகளை சரிபார்க்கவும்.'}
        </p>
      </div>
    </footer>
  );
};
