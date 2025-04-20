
import { AuthForm } from "@/components/auth/AuthForm";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Auth() {
  const navigate = useNavigate();
  
  // Check if user is already logged in
  useEffect(() => {
    const currentUser = localStorage.getItem("property_ai_current_user");
    if (currentUser) {
      navigate("/");
    }
  }, [navigate]);
  
  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-b from-background to-background/90">
      <div className="absolute inset-0 -z-10">
        {/* Background pattern */}
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:20px_20px] opacity-25 dark:bg-[radial-gradient(#1e293b_1px,transparent_1px)]"></div>
      </div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <AuthForm />
      </motion.div>
    </div>
  );
}
