import React, { useState, useEffect } from 'react';
import { X, ShieldCheck } from 'lucide-react';
import { UserProfile, SupportedLanguage } from '../types/api';

interface EligibilityModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmitProfile: (profile: UserProfile) => void;
  isLoading: boolean;
  language?: SupportedLanguage;
}

export const EligibilityModal: React.FC<EligibilityModalProps> = ({
  isOpen,
  onClose,
  onSubmitProfile,
  isLoading,
  language = 'ta',
}) => {
  const isEn = language === 'en';

  const [age, setAge] = useState<string>('');
  const [gender, setGender] = useState<string>('female');
  const [occupation, setOccupation] = useState<string>('student');
  const [isStudent, setIsStudent] = useState<boolean>(true);
  const [isHeadOfFamily, setIsHeadOfFamily] = useState<boolean>(false);
  const [annualIncome, setAnnualIncome] = useState<string>('');
  const [district, setDistrict] = useState<string>(isEn ? 'Chennai' : 'சென்னை');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const profile: UserProfile = {
      gender: gender || undefined,
      occupation: occupation || undefined,
      is_student: isStudent,
      is_head_of_family: isHeadOfFamily,
    };

    if (age.trim() !== '') {
      const parsedAge = parseInt(age, 10);
      if (!isNaN(parsedAge) && parsedAge > 0) {
        profile.age = parsedAge;
      }
    }

    if (annualIncome.trim() !== '') {
      const parsedIncome = parseFloat(annualIncome);
      if (!isNaN(parsedIncome) && parsedIncome >= 0) {
        profile.annual_income = parsedIncome;
      }
    }

    if (district.trim() !== '') {
      profile.district = district.trim();
    }

    onSubmitProfile(profile);
    onClose();
  };

  return (
    <div
      className="modal-overlay"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-heading"
    >
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-group">
            <h2 id="modal-heading" className="modal-title">
              {isEn ? '🎯 Check Your Eligibility' : '🎯 உங்கள் தகுதியை சரிபார்க்கவும்'}
            </h2>
            <p className="modal-subtitle">
              {isEn ? 'Please enter a few basic details.' : 'சில அடிப்படை தகவல்களை மட்டும் உள்ளிடுங்கள்.'}
            </p>
          </div>
          <button
            type="button"
            className="modal-close-btn"
            onClick={onClose}
            aria-label={isEn ? 'Close dialog' : 'சாளரத்தை மூடு'}
          >
            <X size={28} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="eligibility-form">
          <div className="form-grid">
            {/* 1. Age */}
            <div className="form-group">
              <label htmlFor="modal-age" className="form-label">
                {isEn ? 'Age' : 'வயது'}
              </label>
              <input
                id="modal-age"
                type="number"
                min="1"
                max="120"
                placeholder={isEn ? 'e.g. 21' : 'எடுத்துக்காட்டு: 21'}
                value={age}
                onChange={(e) => setAge(e.target.value)}
                className="form-input"
              />
            </div>

            {/* 2. Gender */}
            <div className="form-group">
              <label htmlFor="modal-gender" className="form-label">
                {isEn ? 'Gender' : 'பாலினம்'}
              </label>
              <select
                id="modal-gender"
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                className="form-select"
              >
                <option value="female">{isEn ? 'Female' : 'பெண்'}</option>
                <option value="male">{isEn ? 'Male' : 'ஆண்'}</option>
                <option value="other">{isEn ? 'Other' : 'மற்றவை'}</option>
              </select>
            </div>

            {/* 3. Student Status */}
            <div className="form-group">
              <span className="form-label">{isEn ? 'Are you a student?' : 'நீங்கள் மாணவரா?'}</span>
              <div className="radio-options-row">
                <label className="radio-option">
                  <input
                    type="radio"
                    name="isStudentRadio"
                    checked={isStudent === true}
                    onChange={() => setIsStudent(true)}
                  />
                  <span>{isEn ? 'Yes' : 'ஆம்'}</span>
                </label>
                <label className="radio-option">
                  <input
                    type="radio"
                    name="isStudentRadio"
                    checked={isStudent === false}
                    onChange={() => setIsStudent(false)}
                  />
                  <span>{isEn ? 'No' : 'இல்லை'}</span>
                </label>
              </div>
            </div>

            {/* 4. Head of Family */}
            <div className="form-group">
              <span className="form-label">
                {isEn ? 'Head of household (woman)?' : 'குடும்பத் தலைவியா?'}
              </span>
              <div className="radio-options-row">
                <label className="radio-option">
                  <input
                    type="radio"
                    name="isHeadRadio"
                    checked={isHeadOfFamily === true}
                    onChange={() => setIsHeadOfFamily(true)}
                  />
                  <span>{isEn ? 'Yes' : 'ஆம்'}</span>
                </label>
                <label className="radio-option">
                  <input
                    type="radio"
                    name="isHeadRadio"
                    checked={isHeadOfFamily === false}
                    onChange={() => setIsHeadOfFamily(false)}
                  />
                  <span>{isEn ? 'No' : 'இல்லை'}</span>
                </label>
              </div>
            </div>

            {/* 5. Occupation */}
            <div className="form-group">
              <label htmlFor="modal-occupation" className="form-label">
                {isEn ? 'Occupation' : 'தொழில்'}
              </label>
              <select
                id="modal-occupation"
                value={occupation}
                onChange={(e) => {
                  setOccupation(e.target.value);
                  if (e.target.value === 'student') {
                    setIsStudent(true);
                  }
                }}
                className="form-select"
              >
                <option value="student">{isEn ? 'Student' : 'மாணவர்'}</option>
                <option value="employee">{isEn ? 'Employee' : 'பணியாளர்'}</option>
                <option value="farmer">{isEn ? 'Farmer' : 'விவசாயி'}</option>
                <option value="self_employed">{isEn ? 'Self Employed' : 'சுயதொழில்'}</option>
                <option value="unemployed">{isEn ? 'Unemployed' : 'வேலையில்லாதவர்'}</option>
                <option value="other">{isEn ? 'Other' : 'மற்றவை'}</option>
              </select>
            </div>

            {/* 6. Annual Income */}
            <div className="form-group">
              <label htmlFor="modal-income" className="form-label">
                {isEn ? 'Annual Family Income' : 'ஆண்டு குடும்ப வருமானம்'}
              </label>
              <input
                id="modal-income"
                type="number"
                min="0"
                step="5000"
                placeholder={isEn ? '₹ e.g. 100000' : '₹ எடுத்துக்காட்டு: 100000'}
                value={annualIncome}
                onChange={(e) => setAnnualIncome(e.target.value)}
                className="form-input"
              />
            </div>

            {/* 7. District */}
            <div className="form-group form-group-full">
              <label htmlFor="modal-district" className="form-label">
                {isEn ? 'District' : 'மாவட்டம்'}
              </label>
              <input
                id="modal-district"
                type="text"
                placeholder={isEn ? 'e.g. Chennai, Madurai, Coimbatore' : 'எடுத்துக்காட்டு: சென்னை, மதுரை, கோயம்புத்தூர்'}
                value={district}
                onChange={(e) => setDistrict(e.target.value)}
                className="form-input"
              />
            </div>
          </div>

          <div className="modal-trust-note">
            <span>
              {isEn
                ? '🔒 Your information is used only temporarily during this session.'
                : '🔒 உங்கள் தகவல்கள் இந்த அமர்வில் மட்டும் பயன்படுத்தப்படும்.'}
            </span>
          </div>

          <div className="modal-actions-footer">
            <button
              type="button"
              className="btn-modal-cancel"
              onClick={onClose}
              disabled={isLoading}
            >
              {isEn ? 'Cancel' : 'ரத்து செய்'}
            </button>
            <button type="submit" className="btn-modal-submit" disabled={isLoading}>
              <ShieldCheck size={22} />
              <span>
                {isLoading
                  ? (isEn ? 'Checking...' : 'சரிபார்க்கப்படுகிறது...')
                  : (isEn ? '✓ Check Eligibility' : '✓ தகுதியை சரிபார்க்கவும்')}
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
