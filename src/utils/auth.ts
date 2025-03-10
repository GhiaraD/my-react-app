import { jwtDecode } from "jwt-decode";

interface DecodedToken {
  exp: number;
  role: string;
}

export const getUserRole = (): string | null => {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const decoded: DecodedToken = jwtDecode<DecodedToken>(token);
    return decoded.role;
  } catch (_) {
    return null;
  }
};