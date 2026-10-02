import React from 'react';
import { ExternalLink, Building2 } from 'lucide-react';
import { ChatResponse, MatchedScheme, Eligibility } from '../types/api';

export interface DisplayMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  responseObject?: ChatResponse;
  timestamp?: string;
}

interface ChatMessageProps {
  message: DisplayMessage;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  const resp = message.responseObject;

  const cleanText = (rawText: string) => {
    return rawText.replace(/\*\*/g, '');
  };

  const renderEligibilityStatus = (eligibility?: Eligibility | null) => {
    if (!eligibility) return null;

    const { status, matched_criteria, missing_criteria, required_documents } = eligibility;

    let statusIcon = '🟢';
    let statusText = 'நீங்கள் தகுதியுடையவராக இருக்கலாம்';
    let statusClass = 'status-box-eligible';

    if (status === 'eligible' || status === 'likely_eligible') {
      statusIcon = '🟢';
      statusText = 'நீங்கள் தகுதியுடையவராக இருக்கலாம்';
      statusClass = 'status-box-eligible';
    } else if (status === 'not_eligible') {
      statusIcon = '🔴';
      statusText = 'தற்போதைய தகவல்களின் அடிப்படையில் தகுதி இல்லை';
      statusClass = 'status-box-not-eligible';
    } else if (status === 'needs_more_info') {
      statusIcon = '🟡';
      statusText = 'மேலும் தகவல் தேவை';
      statusClass = 'status-box-needs-info';
    }

    return (
      <div className={`scheme-eligibility-block ${statusClass}`}>
        <div className="eligibility-status-header">
          <span className="status-emoji-icon" aria-hidden="true">{statusIcon}</span>
          <span className="eligibility-status-title">தகுதி நிலை: {statusText}</span>
        </div>

        {/* Criteria list */}
        {(matched_criteria.length > 0 || missing_criteria.length > 0) && (
          <div className="eligibility-criteria-section">
            <h5 className="criteria-subheading">காரணம்:</h5>
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
            <h5 className="documents-subheading">📄 தேவையான ஆவணங்கள்</h5>
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

    return (
      <div key={key} className="scheme-panel">
        {/* Scheme Header */}
        <div className="scheme-panel-header">
          <h4 className="scheme-panel-title">🎓 {cleanText(scheme.title_ta || scheme.title_en)}</h4>
          {scheme.department && (
            <p className="scheme-panel-dept">
              <Building2 size={18} className="inline-icon" /> {cleanText(scheme.department)}
            </p>
          )}
        </div>

        {/* Eligibility Section */}
        {renderEligibilityStatus(schemeElig)}

        {/* Benefits Section */}
        {(scheme.summary_ta || scheme.summary_en) && (
          <div className="scheme-panel-section">
            <h5 className="scheme-section-title">💰 கிடைக்கும் உதவி</h5>
            <p className="scheme-section-text">{cleanText(scheme.summary_ta || scheme.summary_en)}</p>
          </div>
        )}

        {/* Application Steps */}
        {resp?.action_steps && resp.action_steps.length > 0 && (
          <div className="scheme-panel-section">
            <h5 className="scheme-section-title">📍 எப்படி விண்ணப்பிப்பது?</h5>
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
              <span>அதிகாரப்பூர்வ அரசு ஆதாரம்</span>
            </div>
            <a
              href={scheme.official_url}
              target="_blank"
              rel="noopener noreferrer"
              className="official-portal-link-btn"
            >
              <span>🌐 அதிகாரப்பூர்வ தளத்தைத் திறக்கவும்</span>
              <ExternalLink size={20} />
            </a>
          </div>
        )}
      </div>
    );
  };

  const isMultiScheme = (resp?.matched_schemes?.length ?? 0) > 1;

  return (
    <div className={`message-row ${isUser ? 'message-user-row' : 'message-assistant-row'}`}>
      <div className="message-content-wrapper">
        <div className="message-sender-label">
          <span className="sender-name">{isUser ? 'நீங்கள்' : 'NammaSahay AI'}</span>
        </div>

        <div className="message-body-text">{cleanText(message.text)}</div>

        {/* Matched Schemes Information Panels */}
        {resp && resp.matched_schemes && resp.matched_schemes.length > 0 && (
          <div className="response-schemes-wrapper">
            <h3 className="schemes-section-heading">பொருந்தக்கூடிய அரசு நலத்திட்டங்கள்</h3>
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
