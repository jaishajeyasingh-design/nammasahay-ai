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
            தமிழில் அரசு நலத்திட்டங்களை எளிதாக கண்டறியுங்கள்
          </p>
        </div>

        <div className="header-actions">
          {onOpenEligibilityModal && (
            <button
              type="button"
              className="check-eligibility-header-btn"
              onClick={onOpenEligibilityModal}
            >
              🎯 தகுதி சரிபார்ப்பு
            </button>
          )}

          <button
            type="button"
            className="language-toggle-btn"
            onClick={() => onLanguageToggle?.(currentLanguage === 'ta' ? 'en' : 'ta')}
            aria-label="மொழியினை மாற்றவும்"
          >
            <span className={currentLanguage === 'ta' ? 'active-lang' : ''}>தமிழ்</span>
            <span className="lang-divider">|</span>
            <span className={currentLanguage === 'en' ? 'active-lang' : ''}>English</span>
          </button>

          {onFontScaleChange && (
            <div className="font-scale-group" aria-label="உரை அளவு மாற்றி">
              <button
                type="button"
                className={`font-scale-btn ${fontScale === 'normal' ? 'active' : ''}`}
                onClick={() => onFontScaleChange('normal')}
                title="இயல்பு அளவு"
                aria-label="இயல்பு உரை அளவு"
              >
                A-
              </button>
              <button
                type="button"
                className={`font-scale-btn ${fontScale === 'large' ? 'active' : ''}`}
                onClick={() => onFontScaleChange('large')}
                title="பெரிய அளவு"
                aria-label="பெரிய உரை அளவு"
              >
                A
              </button>
              <button
                type="button"
                className={`font-scale-btn ${fontScale === 'xlarge' ? 'active' : ''}`}
                onClick={() => onFontScaleChange('xlarge')}
                title="மிகப் பெரிய அளவு"
                aria-label="மிகப் பெரிய உரை அளவு"
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
