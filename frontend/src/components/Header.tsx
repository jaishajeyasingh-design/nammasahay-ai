import React from 'react';
import { SupportedLanguage } from '../types/api';
import { FontScale } from '../App';

interface HeaderProps {
  currentLanguage?: SupportedLanguage;
  onLanguageToggle?: (lang: SupportedLanguage) => void;
  onOpenEligibilityModal?: () => void;
  fontScale?: FontScale;
  onFontScaleChange?: (scale: FontScale) => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentLanguage = 'ta',
  onLanguageToggle,
  onOpenEligibilityModal,
  fontScale = 'normal',
  onFontScaleChange,
}) => {
  const isEn = currentLanguage === 'en';

  return (
    <header className="header-container" role="banner">
      <div className="header-content">
        <div className="brand-section">
          <div className="brand-title-row">
            <h1 className="brand-title">NammaSahay AI</h1>
            <span className="tricolor-badge" title="Government Scheme Assistant" aria-hidden="true">
              <span className="tc-orange"></span>
              <span className="tc-white"></span>
              <span className="tc-green"></span>
            </span>
          </div>
          <p className="brand-subtitle">
            {isEn
              ? 'Easily discover Tamil Nadu government welfare schemes'
              : 'தமிழில் அரசு நலத்திட்டங்களை எளிதாக கண்டறியுங்கள்'}
          </p>
        </div>

        <div className="header-actions">
          {onOpenEligibilityModal && (
            <button
              type="button"
              className="check-eligibility-header-btn"
              onClick={onOpenEligibilityModal}
            >
              {isEn ? '🎯 Check Eligibility' : '🎯 தகுதி சரிபார்ப்பு'}
            </button>
          )}

          <div className="language-selector-group" aria-label="Language Selector">
            <button
              type="button"
              className={`lang-option-btn ${currentLanguage === 'ta' ? 'active-lang' : ''}`}
              onClick={() => onLanguageToggle?.('ta')}
              aria-label="தமிழ் மொழியைத் தேர்ந்தெடுக்கவும்"
            >
              தமிழ்
            </button>
            <span className="lang-divider">|</span>
            <button
              type="button"
              className={`lang-option-btn ${currentLanguage === 'en' ? 'active-lang' : ''}`}
              onClick={() => onLanguageToggle?.('en')}
              aria-label="Select English language"
            >
              English
            </button>
          </div>

          {onFontScaleChange && (
            <div className="font-scale-group" aria-label={isEn ? 'Text size controls' : 'உரை அளவு மாற்றி'}>
              <button
                type="button"
                className={`font-scale-btn ${fontScale === 'normal' ? 'active' : ''}`}
                onClick={() => onFontScaleChange('normal')}
                title={isEn ? 'Normal size' : 'இயல்பு அளவு'}
                aria-label={isEn ? 'Normal text size' : 'இயல்பு உரை அளவு'}
              >
                A-
              </button>
              <button
                type="button"
                className={`font-scale-btn ${fontScale === 'large' ? 'active' : ''}`}
                onClick={() => onFontScaleChange('large')}
                title={isEn ? 'Large size' : 'பெரிய அளவு'}
                aria-label={isEn ? 'Large text size' : 'பெரிய உரை அளவு'}
              >
                A
              </button>
              <button
                type="button"
                className={`font-scale-btn ${fontScale === 'xlarge' ? 'active' : ''}`}
                onClick={() => onFontScaleChange('xlarge')}
                title={isEn ? 'Extra large size' : 'மிகப் பெரிய அளவு'}
                aria-label={isEn ? 'Extra large text size' : 'மிகப் பெரிய உரை அளவு'}
              >
                A+
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
