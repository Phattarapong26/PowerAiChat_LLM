
import { useState } from "react";
import { Upload, File, CheckCircle, AlertCircle, ArrowUpCircle, Building2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { motion } from "framer-motion";
import { uploadPropertyFile } from "../frontend/api";

export default function FileUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [consultationStyle, setConsultationStyle] = useState<string>("formal");
  const [uploading, setUploading] = useState<boolean>(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const [isDragging, setIsDragging] = useState<boolean>(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      
      // Check if file is an Excel file
      const fileType = selectedFile.name.split('.').pop()?.toLowerCase();
      if (fileType !== 'xlsx' && fileType !== 'xls' && fileType !== 'csv') {
        toast.error("กรุณาอัปโหลดไฟล์ Excel หรือ CSV เท่านั้น");
        e.target.value = '';
        return;
      }
      
      // Check file size (limit to 5MB)
      if (selectedFile.size > 5 * 1024 * 1024) {
        toast.error("ไฟล์ขนาดใหญ่เกินไป (สูงสุด 5MB)");
        e.target.value = '';
        return;
      }
      
      setFile(selectedFile);
      setUploadStatus("idle");
      toast.success("เลือกไฟล์สำเร็จ");
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      
      // Check if file is an Excel file
      const fileType = droppedFile.name.split('.').pop()?.toLowerCase();
      if (fileType !== 'xlsx' && fileType !== 'xls' && fileType !== 'csv') {
        toast.error("กรุณาอัปโหลดไฟล์ Excel หรือ CSV เท่านั้น");
        return;
      }
      
      // Check file size (limit to 5MB)
      if (droppedFile.size > 5 * 1024 * 1024) {
        toast.error("ไฟล์ขนาดใหญ่เกินไป (สูงสุด 5MB)");
        return;
      }
      
      setFile(droppedFile);
      setUploadStatus("idle");
      toast.success("เลือกไฟล์สำเร็จ");
    }
  };

  const handleStyleChange = (value: string) => {
    setConsultationStyle(value);
    toast.info(`เปลี่ยนรูปแบบการให้คำปรึกษาเป็น ${getStyleNameInThai(value)}`);
  };

  const getStyleNameInThai = (style: string) => {
    switch (style) {
      case "formal": return "ทางการ";
      case "casual": return "ทั่วไป";
      case "friendly": return "เป็นกันเอง";
      case "professional": return "มืออาชีพ";
      default: return style;
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    
    try {
      // Call the backend API to upload the file
      const response = await uploadPropertyFile(file, consultationStyle);
      
      setUploadStatus("success");
      toast.success(response.message || "อัปโหลดไฟล์สำเร็จ");
      toast.info(`นำเข้าข้อมูล ${response.num_records} รายการ`);
    } catch (error) {
      console.error("Error uploading file:", error);
      setUploadStatus("error");
      toast.error("เกิดข้อผิดพลาดในการอัปโหลดไฟล์");
    } finally {
      setUploading(false);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full"
    >
      <Card className="w-full max-w-md mx-auto border-blue-200 dark:border-blue-900 overflow-hidden">
        <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/50 dark:to-indigo-950/50">
          <CardTitle className="flex items-center gap-2 text-xl">
            <Building2 className="h-6 w-6 text-#43BE98" />
            อัปโหลดข้อมูลอสังหาริมทรัพย์
          </CardTitle>
          <CardDescription>
            อัปโหลดไฟล์ Excel ที่มีข้อมูลอสังหาริมทรัพย์ของคุณเพื่อใช้ในการวิเคราะห์
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 p-6">
          <div className="grid w-full items-center gap-1.5">
            <Label htmlFor="file" className="mb-1 font-medium">ไฟล์ Excel</Label>
            <motion.div 
              className={`relative border-2 ${isDragging ? 'border-#43BE98 bg-#43BE98/10 dark:bg-#43BE98/5' : 'border-dashed'} rounded-xl p-10 text-center cursor-pointer hover:bg-muted/50 transition-all duration-300 group`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => document.getElementById('file-upload')?.click()}
              whileHover={{ scale: 1.01 }}
              animate={{
                boxShadow: isDragging ? '0 0 0 3px rgba(67, 190, 152, 0.3)' : '0 0 0 0 rgba(0, 0, 0, 0)'
              }}
            >
              <input
                id="file-upload"
                type="file"
                className="hidden"
                accept=".xlsx,.xls,.csv"
                onChange={handleFileChange}
              />
              <div className="flex flex-col items-center gap-3">
                <motion.div 
                  className="p-4 rounded-full bg-#43BE98/20 dark:bg-#43BE98/10"
                  animate={{ y: [0, -5, 0] }}
                  transition={{ repeat: Infinity, repeatType: "reverse", duration: 1.5 }}
                >
                  {file ? (
                    <File className="h-10 w-10 text-#43BE98" />
                  ) : (
                    <ArrowUpCircle className="h-10 w-10 text-#43BE98" />
                  )}
                </motion.div>
                
                <div className="text-sm font-medium">
                  {file ? (
                    <div className="flex items-center gap-2">
                      <span className="text-#43BE98 font-medium">{file.name}</span>
                    </div>
                  ) : (
                    <span>คลิกเพื่อเลือกไฟล์หรือลากไฟล์มาวางที่นี่</span>
                  )}
                </div>
                <span className="text-xs text-muted-foreground">
                  รองรับไฟล์ XLSX, XLS, CSV (สูงสุด 5MB)
                </span>
              </div>
              
              {!file && (
                <motion.div 
                  className="absolute inset-0 bg-#43BE98 opacity-0 rounded-xl"
                  animate={{ 
                    opacity: isDragging ? 0.05 : 0 
                  }}
                />
              )}
            </motion.div>
          </div>
          
          <div className="grid w-full items-center gap-1.5 pt-3">
            <Label htmlFor="consultation-style" className="mb-1 font-medium">รูปแบบการให้คำปรึกษา</Label>
            <Select value={consultationStyle} onValueChange={handleStyleChange}>
              <SelectTrigger id="consultation-style" className="border-#43BE98/30 dark:border-#43BE98/20">
                <SelectValue placeholder="เลือกรูปแบบการให้คำปรึกษา" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="formal">ทางการ</SelectItem>
                <SelectItem value="casual">ทั่วไป</SelectItem>
                <SelectItem value="friendly">เป็นกันเอง</SelectItem>
                <SelectItem value="professional">มืออาชีพ</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          {uploadStatus === "success" && (
            <motion.div 
              className="flex items-center gap-2 bg-green-50 text-green-700 p-3 rounded-lg border border-green-200"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span className="text-sm font-medium">อัปโหลดสำเร็จ</span>
            </motion.div>
          )}
          
          {uploadStatus === "error" && (
            <motion.div 
              className="flex items-center gap-2 bg-red-50 text-red-700 p-3 rounded-lg border border-red-200"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <AlertCircle className="h-5 w-5 text-red-600" />
              <span className="text-sm font-medium">เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง</span>
            </motion.div>
          )}
        </CardContent>
        <CardFooter className="bg-gradient-to-r from-#43BE98/5 to-emerald-50/50 dark:from-#43BE98/10 dark:to-emerald-950/30 px-6 py-4">
          <Button 
            onClick={handleUpload}
            disabled={!file || uploading}
            className="w-full bg-gradient-to-r from-#43BE98 to-emerald-600 hover:from-#43BE98/90 hover:to-emerald-700 transition-all"
          >
            {uploading ? (
              <>
                <motion.div 
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="mr-2"
                >
                  ◌
                </motion.div>
                กำลังอัปโหลด...
              </>
            ) : (
              'อัปโหลด'
            )}
          </Button>
        </CardFooter>
      </Card>
    </motion.div>
  );
}
