import { useState } from 'react';
import axios from 'axios';

const ChatComponent = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newMessage = { sender: "user", text: input };
    setMessages([...messages, newMessage]);

    try {
      const response = await axios.post("http://localhost:8000/api/chat", {
        message: input,
      });
      const botMessage = { sender: "bot", text: response.data.response };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { sender: "bot", text: "Error: Could not get response." }]);
    }

    setInput("");
  };

  return (
    <div className="chat-container" style={{ maxWidth: "600px", margin: "auto" }}>
      <h2>Multi-Agent Chatbot</h2>
      <div className="chat-box" style={{ border: "1px solid #ccc", padding: "10px", minHeight: "300px" }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.sender === "user" ? "right" : "left" }}>
            <b>{msg.sender === "user" ? "You" : "Bot"}:</b> {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} style={{ marginTop: "10px" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          required
          style={{ width: "80%", padding: "8px" }}
        />
        <button type="submit" style={{ padding: "8px" }}>Send</button>
      </form>
    </div>
  );
};

export default ChatComponent;
