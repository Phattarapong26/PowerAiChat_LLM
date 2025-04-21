/**
 * API client for interacting with the AI Property Consultant backend
 */

// Base URL for API calls
const API_BASE_URL = 'http://localhost:8000/api';

// Types
export interface PropertyQuery {
  query: string;
  consultation_style?: string;
  session_id?: string;
  chat_room_id?: string;
  save_message?: boolean;
  timestamp?: number;
  get_history?: boolean;
  language?: string;
  user_id?: string;
}

export interface ChatResponse {
  response: string;
  session_id?: string;
  chat_room_id?: string;
  properties?: Array<Record<string, string>>;
  messages?: Array<{
    role: "user" | "assistant";
    content: string;
    timestamp: number;
    properties?: Array<Record<string, string>>;
  }>;
}

export interface ChatHistory {
  chat_room_id: string;
  messages: Array<{
    role: "user" | "assistant";
    content: string;
    timestamp: number;
    properties?: Array<Record<string, string>>;
  }>;
}

export interface UploadResponse {
  message: string;
  file_id: string;
  num_records: number;
}

export interface ConsultationStyles {
  [key: string]: string;
}

// เพิ่ม interface สำหรับการลงทะเบียนและเข้าสู่ระบบ
export interface UserRegisterRequest {
  name: string;
  email: string;
  password: string;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface UserResponse {
  id: string;
  name: string;
  email: string;
  success: boolean;
  message: string;
}

/**
 * Send a chat message to the AI
 */
export const sendChatMessage = async (queryData: PropertyQuery): Promise<ChatResponse> => {
  try {
    // สร้าง copy ของ queryData เพื่อปรับข้อมูลก่อนส่ง
    const adjustedQueryData = { ...queryData };
    
    // ถ้ามี chat_room_id แต่ไม่มี session_id ให้ใช้ chat_room_id เป็น session_id
    if (adjustedQueryData.chat_room_id && !adjustedQueryData.session_id) {
      adjustedQueryData.session_id = adjustedQueryData.chat_room_id;
      // ลบ chat_room_id ออกเพื่อไม่ให้ API สับสน
      delete adjustedQueryData.chat_room_id;
    }
    
    // เพิ่ม flag เพื่อบอก backend ให้บันทึกข้อความนี้
    adjustedQueryData.save_message = true;
    
    // เพิ่มเวลาปัจจุบันในรูปแบบที่ backend เข้าใจได้
    adjustedQueryData.timestamp = Date.now();
    
    // เพิ่ม user_id ถ้ามี
    const user = JSON.parse(localStorage.getItem("property_ai_current_user") || "{}");
    if (user && user.id) {
      adjustedQueryData.user_id = user.id;
    }
    
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(adjustedQueryData),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    
    // ถ้าได้รับ session_id จาก API แต่ไม่มี chat_room_id ให้ใช้ session_id เป็น chat_room_id
    if (data.session_id && !data.chat_room_id) {
      data.chat_room_id = data.session_id;
    }
    
    return data;
  } catch (error) {
    console.error("Error sending chat message:", error);
    throw new Error("Failed to send message. Please try again.");
  }
};

/**
 * Get chat history for a specific chat room
 */
export const getChatRoomHistory = async (chatRoomId: string): Promise<ChatHistory> => {
  try {
    // เปลี่ยนเป็น POST request ด้วย flag get_history
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: chatRoomId,
        chat_room_id: chatRoomId,
        query: '',  // ส่ง query ว่างเพื่อบ่งชี้ว่าต้องการเรียกประวัติ
        get_history: true,  // flag สำหรับบอก backend ว่าต้องการดึงประวัติ
        consultation_style: localStorage.getItem("consultationStyle") || "formal",
        user_id: JSON.parse(localStorage.getItem("user") || "{}")?.id
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.warn(`API error when fetching chat history: ${response.status} - ${errorText}`);
      
      // สร้าง empty history object สำหรับกรณีที่ API ยังไม่รองรับ
      return {
        chat_room_id: chatRoomId,
        messages: []
      };
    }

    const data = await response.json();
    
    // ถ้าไม่มี messages จะสร้าง empty array
    if (!data.messages) {
      data.messages = [];
    }
    
    return {
      chat_room_id: chatRoomId,
      messages: data.messages
    };
  } catch (error) {
    console.error('Error fetching chat history:', error);
    // สร้าง empty history object แทนที่จะ throw error
    return {
      chat_room_id: chatRoomId,
      messages: []
    };
  }
};

/**
 * Upload property data file
 */
export const uploadPropertyFile = async (
  file: File, 
  consultationStyle: string = 'formal'
): Promise<UploadResponse> => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('consultation_style', consultationStyle);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw new Error('Failed to upload file. Please try again.');
  }
};

/**
 * Get available consultation styles
 */
export const getConsultationStyles = async (): Promise<ConsultationStyles> => {
  try {
    const response = await fetch(`${API_BASE_URL}/styles`);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching consultation styles:', error);
    // Return default styles if API fails
    return {
      formal: "ทางการ",
      casual: "ทั่วไป",
      friendly: "เป็นกันเอง",
      professional: "มืออาชีพ"
    };
  }
};

/**
 * บันทึกประวัติการแชทลงฐานข้อมูล
 */
export const saveChatHistory = async (chatRoomId: string, messages: Array<{
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  properties?: Array<Record<string, string>>;
}>): Promise<boolean> => {
  try {
    console.log("เรียกใช้ API saveChatHistory:", chatRoomId);
    
    // ดึง user_id จาก localStorage
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const userId = user?.id;
    
    // ส่งข้อมูลไปยัง API
    const response = await fetch(`${API_BASE_URL}/save_history`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chat_room_id: chatRoomId,
        messages: messages,
        user_id: userId
      }),
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error("ข้อความผิดพลาด:", errorText);
      return false;
    }
    
    const data = await response.json();
    console.log("บันทึกประวัติสำเร็จ:", data);
    return data.success === true;
  } catch (error) {
    console.error('Error saving chat history:', error);
    // ไม่ throw error เพื่อไม่ให้กระทบกับ UX
    return false;
  }
};

/**
 * ลงทะเบียนผู้ใช้ใหม่
 */
export const registerUser = async (userData: UserRegisterRequest): Promise<UserResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error registering user:', error);
    return {
      id: "",
      name: "",
      email: "",
      success: false,
      message: "เกิดข้อผิดพลาดในการลงทะเบียน กรุณาลองใหม่อีกครั้ง"
    };
  }
};

/**
 * เข้าสู่ระบบ
 */
export const loginUser = async (userData: UserLoginRequest): Promise<UserResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error logging in user:', error);
    return {
      id: "",
      name: "",
      email: "",
      success: false,
      message: "เกิดข้อผิดพลาดในการเข้าสู่ระบบ กรุณาลองใหม่อีกครั้ง"
    };
  }
};
