// src/supabaseClient.js
import { createClient } from "@supabase/supabase-js";

// Lấy key từ biến môi trường để bảo mật hơn
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
