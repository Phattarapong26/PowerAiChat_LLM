import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { MessageSquare, FileUp, Home, TrendingUp, Search, Shield, ArrowRight } from "lucide-react";

const founders = [
  {
    name: "Phattarapong Phengtavee",
    title: "Founder",
    image: "https://github.com/Zx0966566414/image/blob/main/Screenshot%202568-03-28%20at%2013.08.08.png?raw=true",
    delay: 0.1
  },
  {
    name: "Athitaya Chaisiriwattanasai",
    title: "Co-Founder",
    image: "https://github.com/Zx0966566414/image/blob/main/Screenshot%202568-03-28%20at%2012.50.37.png?raw=true",
    delay: 0.2
  },
  {
    name: "Kittipat Pramjit",
    title: "Co-Founder",
    image: "https://github.com/Zx0966566414/image/blob/main/Screenshot%202568-03-28%20at%2012.57.20.png?raw=true",
    delay: 0.3
  }
];
const FeatureCard = ({ icon, title, description, buttonText, onClick, delay }) => {
  return (
    <motion.div
      className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-gray-100 dark:border-gray-700 h-full"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
    >
      <div className="p-2">
        <div className="bg-gradient-to-br from-[#43BE98]/10 to-emerald-400/5 rounded-lg p-6">
          <div className="h-12 w-12 rounded-full bg-[#43BE98] flex items-center justify-center mb-4">
            {icon}
          </div>
          <h3 className="text-xl font-bold mb-2">{title}</h3>
          <p className="text-gray-500 dark:text-gray-400 mb-4">
            {description}
          </p>
          <Button
            onClick={onClick}
            variant={buttonText.includes("เริ่มสนทนา") ? "default" : "outline"}
            className={buttonText.includes("เริ่มสนทนา") ? "w-full bg-[#43BE98] hover:bg-[#3aa988]" : "w-full border-[#43BE98] text-[#43BE98] hover:bg-[#43BE98]/10"}
          >
            {buttonText} <ArrowRight className="h-4 w-4 ml-1" />
          </Button>
        </div>
      </div>
    </motion.div>
  );
};

const Index = () => {
  const navigate = useNavigate();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.3 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <section className="mb-12 lg:mb-20">
        <motion.div
          className="max-w-3xl mx-auto text-center"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="inline-block mb-10 mt-10">
            <span className="px-3 py-1 rounded-full bg-[#43BE98]/20 text-[#43BE98] text-sm font-medium">
              FUNDEE AI
            </span>
          </div>

          <motion.h1
            className="text-4xl md:text-5xl font-bold tracking-tight mb-4 bg-gradient-to-r from-gray-800 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.8 }}
          >
            ผู้ช่วยอัจฉริยะ <span className="text-[#43BE98]">อสังหาริมทรัพย์</span>
          </motion.h1>

          <motion.p
            className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            เพียงถามคำถามสิ่งที่คุณสนใจ เราช่วยให้คุณค้นหาอสังหาได้อย่างมั่นใจ
          </motion.p>

          <motion.div
            className="flex flex-wrap justify-center gap-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            <Button
              onClick={() => navigate("/chat")}
              className="bg-[#43BE98] hover:bg-emerald-600 text-white px-6"
              size="lg"
            >
              <MessageSquare className="mr-2 h-5 w-5" /> เริ่มสนทนากับ AI
            </Button>
            <Button
              onClick={() => navigate("/upload")}
              variant="outline"
              className="border-gray-300 hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-800 px-6"
              size="lg"
            >
              <FileUp className="mr-2 h-5 w-5" /> อัปโหลดข้อมูล
            </Button>
          </motion.div>
        </motion.div>
      </section>

      <motion.section
        className="mb-12"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants} className="text-center mb-10">
          <h2 className="text-2xl font-bold mb-2">บริการของเรา</h2>
          <div className="w-20 h-1 bg-[#43BE98] mx-auto"></div>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Home className="h-6 w-6 text-white" />}
            title="ค้นหาโครงการ"
            description="ค้นพบโครงการที่ตรงใจในทำเลที่คุณต้องการ พร้อมข้อมูลราคา และสิ่งอำนวยความสะดวก"
            buttonText="เริ่มต้นค้นหา"
            onClick={() => navigate("/chat")}
            delay={0.1}
          />

          <FeatureCard
            icon={<MessageSquare className="h-6 w-6 text-white" />}
            title="สนทนากับ AI"
            description="ถามคำถามเกี่ยวกับอสังหาริมทรัพย์ได้ทุกเรื่อง ไม่ว่าจะเป็นเรื่องราคา ทำเล หรือความคุ้มค่าในการลงทุน"
            buttonText="เริ่มสนทนา"
            onClick={() => navigate("/chat")}
            delay={0.2}
          />

          <FeatureCard
            icon={<FileUp className="h-6 w-6 text-white" />}
            title="อัปโหลดข้อมูล"
            description="อัปโหลดข้อมูลอสังหาริมทรัพย์ของคุณ และ AI จะช่วยวิเคราะห์พร้อมให้คำแนะนำที่เหมาะสม"
            buttonText="อัปโหลดข้อมูล"
            onClick={() => navigate("/upload")}
            delay={0.3}
          />
        </div>
      </motion.section>

      <motion.section
        className="mb-12"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8, duration: 0.6 }}
      >
        <div className="p-8 rounded-2xl bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900">
          <div className="max-w-3xl mx-auto">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="flex-1">
                <h3 className="text-2xl font-bold mb-4 flex items-center">
                  <span className="bg-[#43BE98] text-white p-2 rounded-full mr-2">
                    <TrendingUp className="h-4 w-4" />
                  </span>
                  เกี่ยวกับ AI Property Guru
                </h3>
                <p className="mb-4 text-gray-600 dark:text-gray-400">
                  เราคือผู้ช่วยอัจฉริยะด้านอสังหาริมทรัพย์ที่พัฒนาขึ้นด้วยเทคโนโลยี AI ล่าสุด
                  ให้คำแนะนำเกี่ยวกับการซื้อ ขาย เช่า หรือลงทุนในอสังหาริมทรัพย์ได้อย่างแม่นยำ
                </p>
                <div className="flex flex-wrap gap-4 mt-4">
                  <div className="flex items-center">
                    <div className="p-2 rounded-full bg-[#43BE98]/20 mr-2">
                      <Search className="h-4 w-4 text-[#43BE98]" />
                    </div>
                    <span className="text-sm">ค้นหาอสังหาฯ</span>
                  </div>
                  <div className="flex items-center">
                    <div className="p-2 rounded-full bg-[#43BE98]/20 mr-2">
                      <Shield className="h-4 w-4 text-[#43BE98]" />
                    </div>
                    <span className="text-sm">วิเคราะห์อสังหา</span>
                  </div>
                </div>
              </div>
              <div className="md:w-1/3 relative">
                <div className="aspect-square rounded-full bg-[#43BE98]/20 p-4 flex items-center justify-center">
                  <motion.div
                    animate={{
                      scale: [1, 1.05, 1],
                      rotate: [0, 5, 0, -5, 0],
                    }}
                    transition={{
                      duration: 5,
                      repeat: Infinity,
                      repeatType: "reverse"
                    }}
                    className="w-full h-full relative"
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-[#43BE98] to-emerald-400 rounded-full opacity-80"></div>
                    <div className="absolute inset-2 bg-white dark:bg-gray-900 rounded-full flex items-center justify-center">
                      <img
                        src="https://github.com/Phattarapong26/image/blob/main/Screenshot%202568-02-03%20at%2018.03.49.png?raw=true"
                        alt="Logo"
                        className="w-2/3 h-2/3 object-contain"
                      />
                    </div>
                  </motion.div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.section>

      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center max-w-3xl mx-auto mb-16"
          >
            <h1 className="text-3xl text-[#43BE98] font-bold mb-6">OUR FOUNDERS</h1>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {founders.map((founder, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: founder.delay }}
                viewport={{ once: true }}
                className="card text-center"
              >
                <div className="mb-6 rounded-full overflow-hidden w-48 h-48 mx-auto">
                  <img
                    src={founder.image}
                    alt={founder.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <h3 className="heading-sm mb-2">{founder.name}</h3>
                <p className="text-[#43BE98] font-medium">{founder.title}</p>
                <p className="text-gray-400 mt-4">
                  {founder.name === "Phattarapong Phengtavee"
                    ? "I’m committed to transforming the real estate experience with AI-powered insights, making property investment more transparent and accessible for everyone"
                    : founder.name === "Athitiya Chaisiriwatthanachai"
                      ? "I’m passionate about leveraging large language models to simplify complex real estate decisions and bring clarity to every buyer, seller, and investor"
                      : "As a developer and AI enthusiast, I build intelligent chat systems that help people navigate real estate with confidence and ease"}
                </p>

              </motion.div>
            ))}
          </div>
        </div>
      </section>
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 0.8 }}
        className="text-center"
      >
        <h2 className="text-2xl font-bold mb-6">เริ่มต้นใช้งานฟรี</h2>
        <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-lg mx-auto">
          เริ่มต้นใช้งาน AI Property Guru และค้นพบประสบการณ์ใหม่ในการหาข้อมูลอสังหาริมทรัพย์
        </p>
        <Button
          onClick={() => navigate("/chat")}
          className="bg-[#43BE98] hover:bg-emerald-600 text-white px-8"
          size="lg"
        >
          เริ่มต้นใช้งานทันที
        </Button>
      </motion.section>
    </div>
  );
};

export default Index;
