import React from 'react';
import { ExternalLink, Building2 } from 'lucide-react';
import { ChatResponse, MatchedScheme, Eligibility, SupportedLanguage } from '../types/api';

export interface DisplayMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  responseObject?: ChatResponse;
  timestamp?: string;
}

interface ChatMessageProps {
  message: DisplayMessage;
  language?: SupportedLanguage;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message, language = 'ta' }) => {
  const isUser = message.sender === 'user';
  const isEn = language === 'en';
  const resp = message.responseObject;

  const cleanText = (rawText: string) => {
    return rawText.replace(/\*\*/g, '');
  };

  const renderEligibilityStatus = (eligibility?: Eligibility | null) => {
    if (!eligibility) return null;

    const { status, matched_criteria, missing_criteria, required_documents } = eligibility;

    let statusIcon = '🟢';
    let statusText = isEn ? 'You may be eligible' : 'நீங்கள் தகுதியுடையவராக இருக்கலாம்';
    let statusClass = 'status-box-eligible';

    if (status === 'eligible' || status === 'likely_eligible') {
      statusIcon = '🟢';
      statusText = isEn ? 'You may be eligible' : 'நீங்கள் தகுதியுடையவராக இருக்கலாம்';
      statusClass = 'status-box-eligible';
    } else if (status === 'not_eligible') {
      statusIcon = '🔴';
      statusText = isEn ? 'Not eligible based on current details' : 'தற்போதைய தகவல்களின் அடிப்படையில் தகுதி இல்லை';
      statusClass = 'status-box-not-eligible';
    } else if (status === 'needs_more_info') {
      statusIcon = '🟡';
      statusText = isEn ? 'More information required' : 'மேலும் தகவல் தேவை';
      statusClass = 'status-box-needs-info';
    }

    return (
      <div className={`scheme-eligibility-block ${statusClass}`}>
        <div className="eligibility-status-header">
          <span className="status-emoji-icon" aria-hidden="true">{statusIcon}</span>
          <span className="eligibility-status-title">
            {isEn ? 'Eligibility Status:' : 'தகுதி நிலை:'} {statusText}
          </span>
        </div>

        {/* Criteria list */}
        {(matched_criteria.length > 0 || missing_criteria.length > 0) && (
          <div className="eligibility-criteria-section">
            <h5 className="criteria-subheading">{isEn ? 'Reasons / Criteria:' : 'காரணம்:'}</h5>
            <ul className="criteria-bullet-list">
              {matched_criteria.map((item, idx) => (
                <li key={`m-${idx}`} className="criterion-pass">
                  ✓ {cleanText(item)}
                </li>
              ))}
              {missing_criteria.map((item, idx) => (
                <li key={`miss-${idx}`} className="criterion-fail">
                  • {cleanText(item)}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Required Documents */}
        {required_documents && required_documents.length > 0 && (
          <div className="required-documents-section">
            <h5 className="documents-subheading">
              📄 {isEn ? 'Required Documents' : 'தேவையான ஆவணங்கள்'}
            </h5>
            <ul className="documents-bullet-list">
              {required_documents.map((doc, idx) => (
                <li key={idx} className="document-item">
                  ✓ {cleanText(doc)}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const renderSchemePanel = (scheme: MatchedScheme, key: string) => {
    const schemeElig =
      resp?.eligibility_map?.[scheme.scheme_id] ||
      (resp?.matched_schemes?.[0]?.scheme_id === scheme.scheme_id ? resp.eligibility : undefined);

    const title = isEn
      ? (scheme.title_en || scheme.title_ta)
      : (scheme.title_ta || scheme.title_en);

    const summary = isEn
      ? (scheme.summary_en || scheme.summary_ta)
      : (scheme.summary_ta || scheme.summary_en);

    return (
      <div key={key} className="scheme-panel">
        {/* Scheme Header */}
        <div className="scheme-panel-header">
          <h4 className="scheme-panel-title">🎓 {cleanText(title)}</h4>
          {scheme.department && (
            <p className="scheme-panel-dept">
              <Building2 size={18} className="inline-icon" /> {cleanText(scheme.department)}
            </p>
          )}
        </div>

        {/* Eligibility Section */}
        {renderEligibilityStatus(schemeElig)}

        {/* Benefits Section */}
        {summary && (
          <div className="scheme-panel-section">
            <h5 className="scheme-section-title">
              💰 {isEn ? 'Benefits & Financial Support' : 'கிடைக்கும் உதவி'}
            </h5>
            <p className="scheme-section-text">{cleanText(summary)}</p>
          </div>
        )}

        {/* Application Steps */}
        {resp?.action_steps && resp.action_steps.length > 0 && (
          <div className="scheme-panel-section">
            <h5 className="scheme-section-title">
              📍 {isEn ? 'How to Apply' : 'எப்படி விண்ணப்பிப்பது?'}
            </h5>
            <ol className="action-steps-list">
              {resp.action_steps.map((step, idx) => (
                <li key={idx}>{cleanText(step)}</li>
              ))}
            </ol>
          </div>
        )}

        {/* Official Portal Link */}
        {scheme.official_url && (
          <div className="scheme-panel-footer">
            <div className="trust-badge-row">
              <span className="trust-icon">✓</span>
              <span>{isEn ? 'Official Government Source' : 'அதிகாரப்பூர்வ அரசு ஆதாரம்'}</span>
            </div>
            <a
              href={scheme.official_url}
              target="_blank"
              rel="noopener noreferrer"
              className="official-portal-link-btn"
            >
              <span>🌐 {isEn ? 'Open Official Portal' : 'அதிகாரப்பூர்வ தளத்தைத் திறக்கவும்'}</span>
              <ExternalLink size={20} />
            </a>
          </div>
        )}
      </div>
    );
  };

  const isMultiScheme = (resp?.matched_schemes?.length ?? 0) > 1;

  // Determine sender display label
  const senderLabel = isUser
    ? (isEn ? 'You' : 'நீங்கள்')
    : 'NammaSahay AI';

  return (
    <div className={`message-row ${isUser ? 'message-user-row' : 'message-assistant-row'}`}>
      <div className="message-content-wrapper">
        <div className="message-sender-label">
          <span className="sender-name">{senderLabel}</span>
        </div>

        <div className="message-body-text">{cleanText(message.text)}</div>

        {/* Matched Schemes Information Panels */}
        {resp && resp.matched_schemes && resp.matched_schemes.length > 0 && (
          <div className="response-schemes-wrapper">
            <h3 className="schemes-section-heading">
              {isEn ? 'Matching Government Schemes' : 'பொருந்தக்கூடிய அரசு நலத்திட்டங்கள்'}
            </h3>
            <div className={`schemes-grid ${isMultiScheme ? 'multi-scheme-grid' : 'single-scheme-grid'}`}>
              {resp.matched_schemes.map((scheme) =>
                renderSchemePanel(scheme, scheme.scheme_id)
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
