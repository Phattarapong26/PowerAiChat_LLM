import { useState, useEffect } from "react";
import { ChatSession, ChatMessage } from "@/types/chat";
import { useAuth } from "@/context/AuthContext";

const CHAT_STORAGE_KEY = "property_ai_chat_sessions";

export function useChats() {
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const { user } = useAuth();
  
  // Load chat sessions on mount and when user changes
  useEffect(() => {
    if (!user) {
      setChatSessions([]);
      return;
    }
    
    const storedSessions = localStorage.getItem(CHAT_STORAGE_KEY);
    if (storedSessions) {
      try {
        const allSessions: ChatSession[] = JSON.parse(storedSessions);
        // Filter sessions for current user
        const userSessions = allSessions.filter(session => session.userId === user.id);
        setChatSessions(userSessions);
      } catch (error) {
        console.error("Failed to parse stored chat sessions:", error);
        setChatSessions([]);
      }
    }
  }, [user]);
  
  // Save chat sessions whenever they change
  useEffect(() => {
    if (!user) return;
    
    // Get all sessions from storage first
    const storedSessions = localStorage.getItem(CHAT_STORAGE_KEY);
    let allSessions: ChatSession[] = [];
    
    if (storedSessions) {
      try {
        allSessions = JSON.parse(storedSessions);
        // Remove user's sessions from the array
        allSessions = allSessions.filter(session => session.userId !== user.id);
      } catch (error) {
        console.error("Failed to parse stored chat sessions:", error);
        allSessions = [];
      }
    }
    
    // Add current user's sessions back
    allSessions = [...allSessions, ...chatSessions];
    
    // Save all sessions
    localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(allSessions));
  }, [chatSessions, user]);
  
  // Create a new chat session
  const createChatSession = () => {
    if (!user) return null;
    
    const newSession: ChatSession = {
      id: crypto.randomUUID(),
      title: `สนทนา ${new Date().toLocaleString('th-TH')}`,
      createdAt: Date.now(),
      updatedAt: Date.now(),
      messages: [],
      userId: user.id,
      lastUserMessage: null,
      lastAssistantMessage: null,
      messageCount: 0
    };
    
    setChatSessions(prev => [newSession, ...prev]);
    setCurrentChatId(newSession.id);
    return newSession.id;
  };
  
  // Get a chat session by ID
  const getChatSession = (id: string) => {
    return chatSessions.find(session => session.id === id) || null;
  };
  
  // Add a message to a chat session
  const addMessageToChat = (chatId: string, message: Omit<ChatMessage, "id">) => {
    setChatSessions(prev => 
      prev.map(session => {
        if (session.id === chatId) {
          const newMessage: ChatMessage = {
            ...message,
            id: crypto.randomUUID(),
          };
          
          // Update last message based on role
          const updatedSession = {
            ...session,
            messages: [...session.messages, newMessage],
            updatedAt: Date.now(),
            messageCount: session.messageCount + 1
          };

          if (message.role === "user") {
            updatedSession.lastUserMessage = newMessage;
          } else if (message.role === "assistant") {
            updatedSession.lastAssistantMessage = newMessage;
          }

          // Update title with first user message if it's the first message
          if (session.messages.length === 0 && message.role === "user") {
            updatedSession.title = message.content.slice(0, 30) + (message.content.length > 30 ? "..." : "");
          }
          
          return updatedSession;
        }
        return session;
      })
    );
  };
  
  // Delete a chat session
  const deleteChatSession = (chatId: string) => {
    setChatSessions(prev => prev.filter(session => session.id !== chatId));
    if (currentChatId === chatId) {
      setCurrentChatId(null);
    }
  };
  
  return {
    chatSessions,
    currentChatId,
    setCurrentChatId,
    createChatSession,
    getChatSession,
    addMessageToChat,
    deleteChatSession,
  };
}
