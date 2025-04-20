import { useState, useEffect, useContext } from "react";
import {
  ChevronDown,
  Home,
  MessageSquare,
  FileUp,
  Settings,
  HelpCircle,
  LogOut,
  Sparkles,
  ChevronRight,
  History,
  Clock,
  Trash2,
  Plus,
  User,
  Languages,
  Building2,
  HomeIcon,
  Smile,
  Briefcase
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { motion, AnimatePresence } from "framer-motion";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { useAuth } from "@/context/AuthContext";
import { useChats } from "@/hooks/useChats";
import { useToast } from "@/components/ui/use-toast";
import { StyleContext } from "@/components/ChatInterface";

type AIStyle = "formal" | "casual" | "friendly" | "professional";
type Language = "thai" | "english";

interface StyleOption {
  value: AIStyle;
  label: string;
  icon: React.ReactNode;
  description: string;
}

interface LanguageOption {
  value: Language;
  label: string;
  icon: string;
}

export function AppSidebar() {
  const { consultationStyle, setConsultationStyle, language, setLanguage } = useContext(StyleContext);
  const [isStylesOpen, setIsStylesOpen] = useState(false);
  const [isLanguageOpen, setIsLanguageOpen] = useState(false);
  const [isChatHistoryOpen, setIsChatHistoryOpen] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();
  const { chatSessions, setCurrentChatId, deleteChatSession, createChatSession } = useChats();
  const navigate = useNavigate();
  const { toast } = useToast();

  const styleOptions: StyleOption[] = [
    {
      value: "formal",
      label: "ทางการ",
      icon: <Building2 className="h-6 w-6 text-blue-500" />,
      description: "เน้นความสุภาพ ใช้ภาษาทางการ"
    },
    {
      value: "casual",
      label: "ทั่วไป",
      icon: <HomeIcon className="h-6 w-6 text-[#43BE98]" />,
      description: "สบายๆ เป็นธรรมชาติ"
    },
    {
      value: "friendly",
      label: "เป็นกันเอง",
      icon: <Smile className="h-6 w-6 text-[#43BE98]" />,
      description: "เป็นมิตร เหมือนคุยกับเพื่อน"
    },
    {
      value: "professional",
      label: "มืออาชีพ",
      icon: <Briefcase className="h-6 w-6 text-[#43BE98]" />,
      description: "เชี่ยวชาญ ให้ข้อมูลเชิงลึก"
    }
  ];

  const languageOptions: LanguageOption[] = [
    {
      value: "thai",
      label: "ภาษาไทย",
      icon: "🇹🇭"
    },
    {
      value: "english",
      label: "English",
      icon: "🇬🇧"
    }
  ];

  const toggleStyles = () => setIsStylesOpen(!isStylesOpen);
  const toggleLanguage = () => setIsLanguageOpen(!isLanguageOpen);
  const toggleChatHistory = () => setIsChatHistoryOpen(!isChatHistoryOpen);

  const handleLanguageChange = (value: string) => {
    if (value) {
      console.log("เปลี่ยนภาษาเป็น:", value);
      setLanguage(value);
      
      // บันทึกลง localStorage เพื่อให้แน่ใจว่าจะใช้งานได้
      localStorage.setItem("language", value);
      
      toast({
        title: value === "thai" ? "เปลี่ยนภาษาสำเร็จ" : "Language changed successfully",
        description: value === "thai" ? "ภาษาไทยถูกเลือกเป็นภาษาหลัก" : "English is now the primary language",
      });
      
      // ทำให้ UI refresh โดยการเปลี่ยน state บางตัว
      setIsLanguageOpen(false);
      setTimeout(() => setIsLanguageOpen(true), 100);
    }
  };

  const handleLogout = () => {
    logout();
    toast({
      title: "ออกจากระบบสำเร็จ",
      description: "หวังว่าจะได้พบกันใหม่เร็วๆ นี้",
    });
    navigate("/auth");
  };

  const handleNewChat = () => {
    const newChatId = createChatSession();
    if (newChatId) {
      setCurrentChatId(newChatId);
      navigate(`/chat/${newChatId}`);
    } else {
      navigate("/chat");
    }
  };

  const handleChatSelect = (chatId: string) => {
    setCurrentChatId(chatId);
    toast({
      title: "เลือกห้องสนทนา",
      description: `กำลังเปิดห้องสนทนา ID: ${chatId}`,
    });
    localStorage.setItem("chatRoomId", chatId);
    navigate(`/chat/${chatId}`);
  };

  const handleDeleteChat = (chatId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    deleteChatSession(chatId);
    toast({
      title: "ลบสนทนาสำเร็จ",
      description: "สนทนาที่เลือกถูกลบออกแล้ว",
    });
  };

  return (
    <Sidebar className="border-r border-sidebar-border">
      <SidebarHeader>
        <div className="flex items-center gap-3 px-4 py-3">
          <img
            src="https://github.com/Phattarapong26/image/blob/main/Screenshot%202568-02-03%20at%2018.03.49.png?raw=true"
            alt="Logo"
            className="h-25 w-auto"
          />
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-xs uppercase tracking-wider font-semibold text-muted-foreground ml-1 mb-4 border-b">เมนูหลัก</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild className="transition-all hover:translate-x-1">
                  <Link to="/" className="flex items-center">
                    <Home className="text-[#43BE98]" />
                    <span>หน้าหลัก</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton
                  asChild
                  className="transition-all hover:translate-x-1"
                  onClick={handleNewChat}
                >
                  <button className="flex items-center w-full">
                    <MessageSquare className="text-emerald-500" />
                    <span>สนทนากับ AI</span>
                    <Plus className="ml-auto h-4 w-4 text-emerald-500" />
                  </button>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild className="transition-all hover:translate-x-1">
                  <Link to="/upload" className="flex items-center">
                    <FileUp className="text-[#43BE98]" />
                    <span>อัปโหลดข้อมูล</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <div
            className="flex items-center justify-between group cursor-pointer px-2 py-1 rounded-md hover:bg-sidebar-accent transition-colors"
            onClick={toggleStyles}
          >
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-[#43BE98]" />
              <SidebarGroupLabel className="text-xs uppercase tracking-wider font-semibold text-muted-foreground group-hover:text-primary">
                รูปแบบ AI
              </SidebarGroupLabel>
            </div>
            <motion.div
              animate={{ rotate: isStylesOpen ? 90 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <ChevronRight className="h-4 w-4 text-muted-foreground transition-transform duration-200 group-hover:text-primary" />
            </motion.div>
          </div>

          <AnimatePresence>
            {isStylesOpen && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
                className="overflow-hidden"
              >
                <div className="px-2 py-3">
                  <ToggleGroup
                    type="single"
                    value={consultationStyle}
                    onValueChange={(value) => {
                      if (value) {
                        setConsultationStyle(value);
                      }
                    }}
                    className="flex flex-col space-y-2"
                  >
                    {styleOptions.map((style) => (
                      <ToggleGroupItem
                        key={style.value}
                        value={style.value}
                        className={`flex items-start gap-3 p-2 rounded-lg border ${consultationStyle === style.value ? 'border-primary bg-primary/5' : 'border-transparent'} hover:bg-sidebar-accent/70 transition-all w-full h-auto justify-start`}
                      >
                        <div className="w-12 h-12 rounded-md overflow-hidden border border-sidebar-border shrink-0 flex items-center justify-center bg-sidebar-accent/20">
                          {style.icon}
                        </div>
                        <div className="text-left">
                          <div className="font-medium">{style.label}</div>
                          <div className="text-xs text-sidebar-foreground/70">{style.description}</div>
                        </div>
                      </ToggleGroupItem>
                    ))}
                  </ToggleGroup>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <div
            className="flex items-center justify-between group cursor-pointer px-2 py-1 rounded-md hover:bg-sidebar-accent transition-colors"
            onClick={toggleLanguage}
          >
            <div className="flex items-center gap-2">
              <Languages className="h-4 w-4 text-green-500" />
              <SidebarGroupLabel>
                ภาษา
              </SidebarGroupLabel>
            </div>
            <motion.div
              animate={{ rotate: isLanguageOpen ? 90 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <ChevronRight className="h-4 w-4 text-muted-foreground" />
            </motion.div>
          </div>

          <AnimatePresence>
            {isLanguageOpen && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
                className="overflow-hidden"
              >
                <div className="px-2 py-3">
                  <ToggleGroup
                    type="single"
                    value={language}
                    onValueChange={(value) => {
                      if (value) handleLanguageChange(value);
                    }}
                    className="flex flex-col space-y-2"
                  >
                    {languageOptions.map((lang) => (
                      <ToggleGroupItem
                        key={lang.value}
                        value={lang.value}
                        className={`flex items-center gap-3 p-2 rounded-lg ${language === lang.value ? 'bg-primary/10' : ''}`}
                      >
                        <span className="text-2xl">{lang.icon}</span>
                        <span>{lang.label}</span>
                      </ToggleGroupItem>
                    ))}
                  </ToggleGroup>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <div
            className="flex items-center justify-between group cursor-pointer px-2 py-1 rounded-md hover:bg-sidebar-accent transition-colors mt-2"
            onClick={toggleChatHistory}
          >
            <div className="flex items-center gap-2">
              <History className="h-4 w-4 text-[#43BE98]" />
              <SidebarGroupLabel className="text-xs uppercase tracking-wider font-semibold text-muted-foreground group-hover:text-primary">
                ประวัติห้องสนทนา
              </SidebarGroupLabel>
            </div>
            <motion.div
              animate={{ rotate: isChatHistoryOpen ? 90 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <ChevronRight className="h-4 w-4 text-muted-foreground transition-transform duration-200 group-hover:text-primary" />
            </motion.div>
          </div>

          <AnimatePresence>
            {isChatHistoryOpen && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
                className="overflow-hidden"
              >
                <div className="px-2 py-3">
                  {!isAuthenticated ? (
                    <div className="text-center p-2 text-sm text-muted-foreground">
                      กรุณา<Link to="/auth" className="text-primary hover:underline">เข้าสู่ระบบ</Link>เพื่อดูประวัติสนทนา
                    </div>
                  ) : chatSessions.length === 0 ? (
                    <div className="text-center p-2 text-sm text-muted-foreground">
                      ยังไม่มีประวัติห้องสนทนา
                    </div>
                  ) : (
                    <div className="space-y-1 max-h-60 overflow-y-auto pr-1">
                      {chatSessions.map((chat) => (
                        <div
                          key={chat.id}
                          className="flex items-center justify-between p-2 rounded-md hover:bg-sidebar-accent cursor-pointer group"
                          onClick={() => handleChatSelect(chat.id)}
                        >
                          <div className="flex items-center gap-2 truncate">
                            <Clock className="h-4 w-4 text-blue-400 shrink-0" />
                            <span className="text-sm truncate">
                              {chat.title}
                              <span className="text-xs text-muted-foreground ml-1">
                                ({chat.messageCount} ข้อความ)
                              </span>
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            {chat.lastUserMessage && (
                              <span className="text-xs text-muted-foreground truncate max-w-[100px]">
                                {chat.lastUserMessage.content.slice(0, 20)}...
                              </span>
                            )}
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                              onClick={(e) => handleDeleteChat(chat.id, e)}
                            >
                              <Trash2 className="h-4 w-4 text-destructive" />
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild className="transition-all hover:translate-x-1">
                  <Link to="/help" className="flex items-center">
                    <HelpCircle className="text-[#43BE98]" />
                    <span>ช่วยเหลือ</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter className="border-t border-sidebar-border bg-sidebar-accent/20">
        <div className="flex items-center justify-between px-4 py-3">
          {!isAuthenticated ? (
            <div className="flex items-center gap-3">
              <Avatar className="border-2 border-primary/20">
                <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-500 text-white">
                  <User className="h-5 w-5" />
                </AvatarFallback>
              </Avatar>
              <div className="flex flex-col">
                <Link to="/auth" className="text-sm font-medium hover:text-primary">เข้าสู่ระบบ</Link>
                <span className="text-xs text-muted-foreground">ใช้งานแบบไม่ระบุตัวตน</span>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Avatar className="border-2 border-primary/20">
                <AvatarImage src={`https://api.dicebear.com/7.x/thumbs/svg?seed=${user?.name}`} />
                <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-500 text-white">
                  {user?.name.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div className="flex flex-col">
                <span className="text-sm font-medium">{user?.name}</span>
                <span className="text-xs text-muted-foreground truncate max-w-28">{user?.email}</span>
              </div>
            </div>
          )}

          {isAuthenticated && (
            <Button
              variant="ghost"
              size="icon"
              className="rounded-full hover:bg-primary/10 hover:text-primary"
              onClick={handleLogout}
            >
              <LogOut className="h-5 w-5" />
            </Button>
          )}
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
