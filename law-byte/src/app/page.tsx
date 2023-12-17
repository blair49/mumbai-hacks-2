"use client"
import React, { useState, useEffect } from 'react';
import styles from './ChatPage.module.css';

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<{ text: string; user: string }[]>([]);
  const [inputText, setInputText] = useState<string>('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(e.target.value);
  };

  const sendMessage = async () => {
    if (inputText.trim() === '') return;

    setMessages((prevMessages) => [
      ...prevMessages,
      { text: inputText, user: 'user' },
    ]);
    setInputText('');

    const aiResponse = await generateAIResponse(inputText);
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: aiResponse, user: 'ai' },
    ]);
  };

  const generateAIResponse = async (userMessage: string): Promise<string> => {
    try {
      const apiUrl = 'http://127.0.0.1:5000/api/generate_response';
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input:userMessage }),
      });
  
      if (!response.ok) {
        throw new Error(`Failed to fetch AI response. Status: ${response.status}`);
      }
  
      const responseData = await response.json();
  
      const aiResponse = responseData.response;
  
      return aiResponse;
    } catch (error:any) {
      console.error('Error generating AI response:', error.message);
      return 'Error generating AI response';
    }
  };
  

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  // Scroll to the bottom of the chat when messages change
  useEffect(() => {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [messages]);

  return (
    <div className={styles.chatApp}>
      <div><span className={styles.chatTitle}>Byte Law</span> by team Byte Logic.</div>
      <div className={styles.chatPage}>
        <div id="chat-container" className={styles.chatContainer}>
          {messages.map((message, index) => (
            <div key={index} className={`${styles.message} ${styles[message.user]}`}>
              {message.text}
            </div>
          ))}
        </div>
        <div className={styles.inputContainer}>
          <input
            type="text"
            placeholder="Type your query..."
            value={inputText}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            className={styles.inputField}
          />
          <button onClick={sendMessage} className={styles.button}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
