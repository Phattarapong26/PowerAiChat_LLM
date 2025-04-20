
import { useState } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Eye, EyeOff, Mail, Lock, User } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/components/ui/use-toast";

// Simple mock user storage for demo purposes
const USERS_STORAGE_KEY = "property_ai_users";
const CURRENT_USER_KEY = "property_ai_current_user";

interface User {
  id: string;
  email: string;
  name: string;
  password: string; // In a real app, this would be hashed
}

export function AuthForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

  // Login form state
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  // Register form state
  const [registerName, setRegisterName] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");

  const toggleShowPassword = () => setShowPassword(!showPassword);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    setTimeout(() => {
      const usersJson = localStorage.getItem(USERS_STORAGE_KEY);
      const users: User[] = usersJson ? JSON.parse(usersJson) : [];
      
      const user = users.find(u => u.email === loginEmail && u.password === loginPassword);
      
      if (user) {
        // Store current user
        localStorage.setItem(CURRENT_USER_KEY, JSON.stringify({
          id: user.id,
          email: user.email,
          name: user.name
        }));
        
        toast({
          title: "เข้าสู่ระบบสำเร็จ",
          description: `ยินดีต้อนรับกลับ ${user.name}`,
        });
        
        navigate("/");
      } else {
        toast({
          title: "เข้าสู่ระบบไม่สำเร็จ",
          description: "อีเมลหรือรหัสผ่านไม่ถูกต้อง",
          variant: "destructive",
        });
      }
      
      setIsLoading(false);
    }, 1000);
  };

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    setTimeout(() => {
      const usersJson = localStorage.getItem(USERS_STORAGE_KEY);
      const users: User[] = usersJson ? JSON.parse(usersJson) : [];
      
      // Check if email already exists
      if (users.some(u => u.email === registerEmail)) {
        toast({
          title: "ลงทะเบียนไม่สำเร็จ",
          description: "อีเมลนี้ถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น",
          variant: "destructive",
        });
        setIsLoading(false);
        return;
      }
      
      // Create new user
      const newUser: User = {
        id: crypto.randomUUID(),
        email: registerEmail,
        name: registerName,
        password: registerPassword,
      };
      
      users.push(newUser);
      localStorage.setItem(USERS_STORAGE_KEY, JSON.stringify(users));
      
      // Log user in
      localStorage.setItem(CURRENT_USER_KEY, JSON.stringify({
        id: newUser.id,
        email: newUser.email,
        name: newUser.name
      }));
      
      toast({
        title: "ลงทะเบียนสำเร็จ",
        description: "ยินดีต้อนรับสู่ระบบ AI Property Guru",
      });
      
      navigate("/");
      setIsLoading(false);
    }, 1000);
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <Tabs defaultValue="login">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle className="text-4xl"><img 
            src="https://github.com/Phattarapong26/image/blob/main/Screenshot%202568-02-03%20at%2018.03.49.png?raw=true" 
            alt="Logo" 
            className="h-20 w-auto"
          /></CardTitle>
            <TabsList>
              <TabsTrigger value="login">เข้าสู่ระบบ</TabsTrigger>
              <TabsTrigger value="register">ลงทะเบียน</TabsTrigger>
            </TabsList>
          </div>
          <CardDescription>
            เราคือเพื่อนคู่อสังหาของคุณ..
          </CardDescription>
        </CardHeader>

        <CardContent>
          <TabsContent value="login">
            <form onSubmit={handleLogin}>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">อีเมล</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="email"
                      placeholder="your.email@example.com"
                      type="email"
                      className="pl-10"
                      value={loginEmail}
                      onChange={(e) => setLoginEmail(e.target.value)}
                      required
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="password">รหัสผ่าน</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      className="pl-10 pr-10"
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                      required
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="absolute right-1 top-1"
                      onClick={toggleShowPassword}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                      <span className="sr-only">
                        {showPassword ? "Hide password" : "Show password"}
                      </span>
                    </Button>
                  </div>
                </div>
              </div>
              
              <Button
                type="submit"
                className="w-full mt-6 bg-gradient-to-r from-[#43BE98] to-emerald-400"
                disabled={isLoading}
              >
                {isLoading ? "กำลังดำเนินการ..." : "เข้าสู่ระบบ"}
              </Button>
            </form>
          </TabsContent>

          <TabsContent value="register">
            <form onSubmit={handleRegister}>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">ชื่อ</Label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="name"
                      placeholder="ชื่อที่ใช้แสดง"
                      className="pl-10"
                      value={registerName}
                      onChange={(e) => setRegisterName(e.target.value)}
                      required
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="register-email">อีเมล</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="register-email"
                      placeholder="your.email@example.com"
                      type="email"
                      className="pl-10"
                      value={registerEmail}
                      onChange={(e) => setRegisterEmail(e.target.value)}
                      required
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="register-password">รหัสผ่าน</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="register-password"
                      type={showPassword ? "text" : "password"}
                      className="pl-10 pr-10"
                      value={registerPassword}
                      onChange={(e) => setRegisterPassword(e.target.value)}
                      required
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="absolute right-1 top-1"
                      onClick={toggleShowPassword}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                      <span className="sr-only">
                        {showPassword ? "Hide password" : "Show password"}
                      </span>
                    </Button>
                  </div>
                </div>
              </div>
              
              <Button
                type="submit"
                className="w-full mt-6 bg-gradient-to-r from-[#43BE98] to-emerald-400"
                disabled={isLoading}
              >
                {isLoading ? "กำลังดำเนินการ..." : "ลงทะเบียน"}
              </Button>
            </form>
          </TabsContent>
        </CardContent>
      </Tabs>
    </Card>
  );
}
