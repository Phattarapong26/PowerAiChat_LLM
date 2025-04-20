export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  properties?: Array<Record<string, any>>;
}

export interface ChatSession {
  id: string;
  title: string;
  createdAt: number;
  updatedAt: number;
  messages: ChatMessage[];
  userId: string;
  lastUserMessage: ChatMessage | null;
  lastAssistantMessage: ChatMessage | null;
  messageCount: number;
}
