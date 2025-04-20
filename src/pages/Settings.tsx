
import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Bell, User, Shield, Globe, Moon, Key, Languages, Save } from "lucide-react";

const Settings = () => {
  const [profileData, setProfileData] = useState({
    name: "ผู้ใช้งาน",
    email: "user@example.com",
    bio: "นักลงทุนอสังหาริมทรัพย์",
    language: "thai",
  });

  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    marketing: false,
    newProperty: true,
  });

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setProfileData(prev => ({ ...prev, [name]: value }));
  };

  const handleNotificationChange = (key: string) => {
    setNotifications(prev => ({ ...prev, [key]: !prev[key as keyof typeof notifications] }));
  };

  return (
    <div className="container max-w-5xl mx-auto">
      <div className="flex flex-col gap-2 mb-6">
        <h1 className="text-3xl font-bold tracking-tight">ตั้งค่า</h1>
        <p className="text-muted-foreground">จัดการการตั้งค่าบัญชี, ความปลอดภัย และการแจ้งเตือนของคุณ</p>
      </div>

      <Tabs defaultValue="profile" className="space-y-4">
        <TabsList className="grid w-full max-w-md grid-cols-4 h-auto p-1 gap-1">
          <TabsTrigger value="profile" className="flex flex-col items-center py-2 px-1 h-auto">
            <User className="h-5 w-5 mb-1" />
            <span>โปรไฟล์</span>
          </TabsTrigger>
          <TabsTrigger value="notifications" className="flex flex-col items-center py-2 px-1 h-auto">
            <Bell className="h-5 w-5 mb-1" />
            <span>การแจ้งเตือน</span>
          </TabsTrigger>
          <TabsTrigger value="security" className="flex flex-col items-center py-2 px-1 h-auto">
            <Shield className="h-5 w-5 mb-1" />
            <span>ความปลอดภัย</span>
          </TabsTrigger>
          <TabsTrigger value="appearance" className="flex flex-col items-center py-2 px-1 h-auto">
            <Globe className="h-5 w-5 mb-1" />
            <span>การแสดงผล</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="profile" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>ข้อมูลโปรไฟล์</CardTitle>
              <CardDescription>จัดการข้อมูลส่วนตัวของคุณและวิธีที่จะแสดงให้ผู้อื่นเห็น</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex flex-col md:flex-row gap-8">
                <div className="flex flex-col items-center space-y-2">
                  <Avatar className="w-24 h-24 border-4 border-primary/10">
                    <AvatarImage src="https://i.pravatar.cc/200" />
                    <AvatarFallback className="text-2xl bg-gradient-to-br from-blue-500 to-purple-500 text-white">TH</AvatarFallback>
                  </Avatar>
                  <Button variant="outline" size="sm" className="mt-2">เปลี่ยนรูปภาพ</Button>
                </div>

                <div className="space-y-4 flex-1">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">ชื่อ</Label>
                      <Input 
                        id="name" 
                        name="name" 
                        value={profileData.name} 
                        onChange={handleProfileChange} 
                        className="focus-visible:ring-blue-500"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">อีเมล</Label>
                      <Input 
                        id="email" 
                        name="email" 
                        type="email" 
                        value={profileData.email} 
                        onChange={handleProfileChange}
                        className="focus-visible:ring-blue-500"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="bio">เกี่ยวกับ</Label>
                    <Textarea 
                      id="bio" 
                      name="bio" 
                      value={profileData.bio} 
                      onChange={handleProfileChange}
                      placeholder="เขียนบางอย่างเกี่ยวกับตัวคุณ..."
                      className="min-h-[120px] focus-visible:ring-blue-500"
                    />
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-end border-t p-4">
              <Button className="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-600">
                <Save className="w-4 h-4 mr-2" />
                บันทึกการเปลี่ยนแปลง
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>การแจ้งเตือน</CardTitle>
              <CardDescription>กำหนดวิธีที่คุณจะได้รับการแจ้งเตือนจากระบบ</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>การแจ้งเตือนทางอีเมล</Label>
                    <p className="text-sm text-muted-foreground">รับการแจ้งเตือนผ่านทางอีเมล</p>
                  </div>
                  <Switch 
                    checked={notifications.email}
                    onCheckedChange={() => handleNotificationChange('email')}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>การแจ้งเตือนผลักดัน</Label>
                    <p className="text-sm text-muted-foreground">รับการแจ้งเตือนบนอุปกรณ์ของคุณ</p>
                  </div>
                  <Switch 
                    checked={notifications.push}
                    onCheckedChange={() => handleNotificationChange('push')}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>อีเมลการตลาด</Label>
                    <p className="text-sm text-muted-foreground">รับข้อมูลเกี่ยวกับผลิตภัณฑ์และบริการใหม่</p>
                  </div>
                  <Switch 
                    checked={notifications.marketing}
                    onCheckedChange={() => handleNotificationChange('marketing')}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>อสังหาริมทรัพย์ใหม่</Label>
                    <p className="text-sm text-muted-foreground">รับการแจ้งเตือนเมื่อมีอสังหาริมทรัพย์ใหม่ที่ตรงกับความสนใจของคุณ</p>
                  </div>
                  <Switch 
                    checked={notifications.newProperty}
                    onCheckedChange={() => handleNotificationChange('newProperty')}
                  />
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-end border-t p-4">
              <Button className="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-600">
                <Save className="w-4 h-4 mr-2" />
                บันทึกการเปลี่ยนแปลง
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>ความปลอดภัย</CardTitle>
              <CardDescription>จัดการความปลอดภัยของบัญชีของคุณ</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="current-password">รหัสผ่านปัจจุบัน</Label>
                    <Input id="current-password" type="password" className="focus-visible:ring-blue-500" />
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="new-password">รหัสผ่านใหม่</Label>
                    <Input id="new-password" type="password" className="focus-visible:ring-blue-500" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="confirm-password">ยืนยันรหัสผ่านใหม่</Label>
                    <Input id="confirm-password" type="password" className="focus-visible:ring-blue-500" />
                  </div>
                </div>

                <div className="pt-4 border-t">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label className="text-base">การยืนยันตัวตนสองชั้น</Label>
                      <p className="text-sm text-muted-foreground">เพิ่มความปลอดภัยให้กับบัญชีของคุณด้วยการยืนยันตัวตนสองชั้น</p>
                    </div>
                    <Button variant="outline" className="border-blue-500 text-blue-500">
                      <Key className="w-4 h-4 mr-2" />
                      ตั้งค่า
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-end border-t p-4">
              <Button className="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-600">
                <Save className="w-4 h-4 mr-2" />
                อัพเดทรหัสผ่าน
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="appearance" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>การแสดงผล</CardTitle>
              <CardDescription>ปรับแต่งรูปแบบการแสดงผลและภาษาที่ใช้ในแอปพลิเคชัน</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="text-base">ธีมมืด</Label>
                    <p className="text-sm text-muted-foreground">เปิดใช้งานธีมมืดหรือสว่าง</p>
                  </div>
                  <Button variant="outline" className="border-blue-500 text-blue-500">
                    <Moon className="w-4 h-4 mr-2" />
                    เปลี่ยนธีม
                  </Button>
                </div>

                <div className="pt-4 border-t">
                  <div className="space-y-2">
                    <Label htmlFor="language">ภาษา</Label>
                    <div className="flex items-center gap-4">
                      <Button 
                        variant={profileData.language === "thai" ? "default" : "outline"}
                        onClick={() => setProfileData(prev => ({ ...prev, language: "thai" }))}
                        className={profileData.language === "thai" 
                          ? "bg-gradient-to-r from-blue-600 to-blue-500" 
                          : "border-blue-500 text-blue-500"}
                      >
                        <Languages className="w-4 h-4 mr-2" />
                        ไทย
                      </Button>
                      <Button 
                        variant={profileData.language === "english" ? "default" : "outline"}
                        onClick={() => setProfileData(prev => ({ ...prev, language: "english" }))}
                        className={profileData.language === "english" 
                          ? "bg-gradient-to-r from-blue-600 to-blue-500" 
                          : "border-blue-500 text-blue-500"}
                      >
                        <Languages className="w-4 h-4 mr-2" />
                        English
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-end border-t p-4">
              <Button className="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-600">
                <Save className="w-4 h-4 mr-2" />
                บันทึกการเปลี่ยนแปลง
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Settings;
