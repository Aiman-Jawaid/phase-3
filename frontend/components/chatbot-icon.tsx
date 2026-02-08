import React, { useState } from 'react';
import { FaCommentDots } from 'react-icons/fa';

const ChatbotIcon = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChatPanel = () => {
    setIsOpen(!isOpen);
    // Dispatch event to open/close chat panel
    window.dispatchEvent(new CustomEvent('toggleChatPanel', { detail: { isOpen: !isOpen } }));
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <button
        onClick={toggleChatPanel}
        className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 shadow-lg transition-all duration-300 transform hover:scale-105"
        aria-label="Open chatbot"
      >
        <FaCommentDots size={24} />
      </button>
    </div>
  );
};

export default ChatbotIcon;