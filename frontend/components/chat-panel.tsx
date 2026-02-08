import React, { useState, useEffect, useRef } from 'react';
import { FaTimes, FaPaperPlane } from 'react-icons/fa';
import MessageBubbles from './message-bubbles';
import { useConversation } from '../hooks/use-conversation';
import { chatAPI } from '../lib/chat-api';

interface ChatPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatPanel = ({ isOpen, onClose }: ChatPanelProps) => {
  const [inputMessage, setInputMessage] = useState('');
  const { messages, sendMessage, isLoading, currentConversationId, clearMessages } = useConversation();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputMessage.trim()) return;

    await sendMessage(inputMessage);
    setInputMessage('');
  };

  const handleClearChat = () => {
    clearMessages();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-full md:w-96 bg-white shadow-xl z-50 flex flex-col border-l border-gray-200">
      <div className="flex justify-between items-center p-4 bg-blue-600 text-white">
        <h2 className="text-lg font-semibold">AI Todo Assistant</h2>
        <div className="flex space-x-2">
          <button
            onClick={handleClearChat}
            className="text-sm bg-blue-700 hover:bg-blue-800 px-2 py-1 rounded"
            disabled={isLoading}
          >
            Clear
          </button>
          <button
            onClick={onClose}
            className="text-xl hover:bg-blue-700 rounded-full w-8 h-8 flex items-center justify-center"
          >
            <FaTimes />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        {messages.length > 0 ? (
          <MessageBubbles messages={messages} />
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-gray-500">
            <p className="mb-4">Start a conversation with your AI assistant</p>
            <p className="text-sm">Try: "Add a task to buy groceries"</p>
            <p className="text-sm">Try: "Show my pending tasks"</p>
            <p className="text-sm">Try: "Complete task 1"</p>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200 bg-white">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white rounded-lg px-4 py-2 hover:bg-blue-700 disabled:opacity-50"
            disabled={isLoading || !inputMessage.trim()}
          >
            <FaPaperPlane />
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          {isLoading && 'AI is thinking...'}
        </div>
      </form>
    </div>
  );
};

export default ChatPanel;