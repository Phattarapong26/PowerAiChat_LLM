import { useState, useEffect } from "react";
import ChatInterface from "@/components/ChatInterface";
import { Card } from "@/components/ui/card";
import { useChats } from "@/hooks/useChats";
import { useAuth } from "@/context/AuthContext";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "@/components/ui/use-toast";
import { MessageSquare } from "lucide-react";

export default function Chat() {
  const { currentChatId, createChatSession, getChatSession, setCurrentChatId } = useChats();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { id: chatIdFromUrl } = useParams();
  
  useEffect(() => {
    // ถ้ามี ID จาก URL ให้ตั้งค่าเป็น currentChatId
    if (chatIdFromUrl) {
      setCurrentChatId(chatIdFromUrl);
    } else if (!currentChatId) {
      // ถ้าไม่มี ID จาก URL และไม่มี currentChatId ให้สร้างห้องแชทใหม่
      const newChatId = createChatSession();
      if (newChatId) {
        navigate(`/chat/${newChatId}`);
      }
    }
  }, [chatIdFromUrl, currentChatId, createChatSession, navigate, setCurrentChatId]);
  
  return (
    <div className="container max-w-6xl mx-auto mt-[30px]">
      <Card className="p-4 md:p-6">
        <h1 className="text-2xl font-bold mb-6 text-[#43BE98] flex items-center gap-2">
          <MessageSquare className="w-6 h-6" />
          Chat AI<span className="text-gray-400 text-sm"> พูดคุยกับเพื่อนคู่คิดของคุณ...</span>
        </h1>
        <ChatInterface />
      </Card>
    </div>
  );
}

