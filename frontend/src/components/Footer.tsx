import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="footer-container" role="contentinfo">
      <div className="footer-content">
        <p className="footer-trust">
          🔒 NammaSahay AI • தமிழ்நாடு அரசு நலத்திட்ட வழிகாட்டி
        </p>
        <p className="footer-disclaimer">
          தகவல்கள் வழிகாட்டலுக்கு மட்டுமே. விண்ணப்பிக்கும் முன் அதிகாரப்பூர்வ அரசு அறிவிப்புகளை சரிபார்க்கவும்.
        </p>
      </div>
    </footer>
  );
};
