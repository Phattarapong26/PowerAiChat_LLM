
import { motion } from "framer-motion";
import FileUploader from "@/components/FileUploader";
import { FileUpIcon, Building, ChartBar } from "lucide-react";

const UploadPage = () => {
  const features = [
    {
      icon: <FileUpIcon className="h-8 w-8 text-amber-500" />,
      title: "อัปโหลดไฟล์ง่าย",
      description: "รองรับไฟล์ Excel และ CSV เพื่อนำเข้าข้อมูลอสังหาริมทรัพย์"
    },
    {
      icon: <Building className="h-8 w-8 text-emerald-500" />,
      title: "จัดการทรัพย์สิน",
      description: "ระบบจะช่วยจัดการและวิเคราะห์ข้อมูลทรัพย์สินของคุณ"
    },
    {
      icon: <ChartBar className="h-8 w-8 text-blue-500" />,
      title: "รายงานอัจฉริยะ",
      description: "รับรายงานและการวิเคราะห์ที่ทันสมัยจาก AI ของเรา"
    }
  ];

  return (
    <div className="container mx-auto py-6 px-4">
      <motion.div 
        className="max-w-4xl mx-auto space-y-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.div 
          className="flex flex-col gap-2 mb-6"
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-amber-100 dark:bg-amber-900/30">
              <FileUpIcon className="h-8 w-8 text-[#43BE98] dark:text-[#43BE98]" />
            </div>
            <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-[#43BE98] to-[#39b991] bg-clip-text text-transparent">
              อัปโหลดข้อมูลอสังหาริมทรัพย์
            </h1>
          </div>
          <p className="text-muted-foreground">
            อัปโหลดข้อมูลอสังหาริมทรัพย์ของคุณเพื่อรับการวิเคราะห์และคำแนะนำจาก AI Property Guru
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="bg-white dark:bg-blue-950/20 rounded-xl p-6 shadow-sm border border-blue-100 dark:border-blue-900/30"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2 + index * 0.1 }}
              whileHover={{ y: -5, boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)" }}
            >
              <div className="p-3 rounded-lg bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 mb-4 inline-block">
                {feature.icon}
              </div>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-100/20 to-amber-100/20 dark:from-blue-900/10 dark:to-amber-900/10 rounded-2xl -z-10 blur-xl"></div>
          <motion.div 
            className="bg-gradient-to-br from-white to-blue-50/50 dark:from-blue-950/50 dark:to-blue-900/10 border border-blue-100 dark:border-blue-900/30 rounded-2xl p-8 relative overflow-hidden"
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <div className="absolute top-0 right-0 w-40 h-40 bg-gradient-to-br from-amber-200/20 to-amber-400/10 rounded-full blur-3xl -z-10"></div>
            <div className="absolute bottom-0 left-0 w-60 h-60 bg-gradient-to-tr from-blue-200/20 to-blue-400/10 rounded-full blur-3xl -z-10"></div>
            
            <FileUploader />
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
};

export default UploadPage;
