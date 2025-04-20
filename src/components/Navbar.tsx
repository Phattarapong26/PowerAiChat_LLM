
import { Bell, Menu, Search, LogIn, User, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ThemeSwitcher } from "@/components/ThemeSwitcher";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { useIsMobile } from "@/hooks/use-mobile";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { useToast } from "@/components/ui/use-toast";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";

export default function Navbar() {
  const isMobile = useIsMobile();
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const handleLogout = () => {
    logout();
    toast({
      title: "ออกจากระบบสำเร็จ",
      description: "หวังว่าจะได้พบกันใหม่เร็วๆ นี้",
    });
    navigate("/");
  };
  
  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 shadow-sm">
      <div className="container flex h-24 items-center px-4">
        <SidebarTrigger>
          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
            <span className="sr-only">Toggle sidebar</span>
          </Button>
        </SidebarTrigger>
        
        <div className="flex items-center space-x-3">
          <img 
            src="https://github.com/Phattarapong26/image/blob/main/Screenshot%202568-02-03%20at%2018.03.49.png?raw=true" 
            alt="Logo" 
            className="h-14 w-auto"
          />
          <div className="hidden md:block">
            <span className="text-lg font-semibold bg-gradient-to-r from-[#43BE98] to-emerald-400 bg-clip-text text-transparent">
              สวัสดี AI Property Guru
            </span>
          </div>
        </div>
        
        <div className="ml-auto flex items-center gap-4">
          
          
          <ThemeSwitcher />
          
          {isAuthenticated ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8 border border-[#43BE98]/20">
                    <AvatarImage src={`https://api.dicebear.com/7.x/thumbs/svg?seed=${user?.name}`} />
                    <AvatarFallback className="bg-gradient-to-br from-[#43BE98] to-emerald-500 text-white">
                      {user?.name.charAt(0).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <div className="flex flex-col space-y-1 p-2">
                  <p className="text-sm font-medium leading-none">{user?.name}</p>
                  <p className="text-xs leading-none text-muted-foreground">
                    {user?.email}
                  </p>
                </div>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                  <Link to="/settings">
                    ตั้งค่าโปรไฟล์
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleLogout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>ออกจากระบบ</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Button 
              variant="default" 
              size={isMobile ? "sm" : "default"}
              className="bg-gradient-to-r from-[#43BE98] to-emerald-400 hover:from-emerald-400 hover:to-[#43BE98] transition-all"
              onClick={() => navigate("/auth")}
            >
              <LogIn className="h-4 w-4 mr-2" />
              เข้าสู่ระบบ
            </Button>
          )}
        </div>
      </div>
    </header>
  );
}
