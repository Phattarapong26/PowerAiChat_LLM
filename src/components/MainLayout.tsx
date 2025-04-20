
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import Navbar from "@/components/Navbar";
import { Outlet } from "react-router-dom";
import { motion } from "framer-motion";

export default function MainLayout() {
  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-gradient-to-br from-background to-background/95 overflow-hidden">
        <AppSidebar />
        <div className="flex flex-col flex-1 relative">
          <Navbar />
          <motion.main 
            className="flex-1 px-4 py-6 md:px-8 overflow-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Outlet />
          </motion.main>
          <div className="absolute inset-0 -z-10">
            {/* Background pattern */}
            <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:20px_20px] opacity-25 dark:bg-[radial-gradient(#1e293b_1px,transparent_1px)]"></div>
            
            {/* Animated gradient blobs */}
            <motion.div 
              className="absolute top-20 left-10 w-64 h-64 rounded-full bg-[#43BE98]/10 blur-3xl"
              animate={{ 
                x: [0, 50, 0],
                y: [0, 30, 0],
              }}
              transition={{ 
                duration: 20, 
                repeat: Infinity,
                repeatType: "reverse" 
              }}
            />
            <motion.div 
              className="absolute bottom-20 right-10 w-80 h-80 rounded-full bg-emerald-400/10 blur-3xl"
              animate={{ 
                x: [0, -40, 0],
                y: [0, -20, 0],
              }}
              transition={{ 
                duration: 15, 
                repeat: Infinity,
                repeatType: "reverse" 
              }}
            />
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
}
