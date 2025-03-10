import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUserRole } from "../utils/auth"; // Import the function

const Dashboard: React.FC = () => {
  const [userRole, setUserRole] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const role = getUserRole(); // Call the function
    setUserRole(role);

    if (!role) {
      navigate("/login"); // Redirect if no role is found
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div>
      <h2>Dashboard</h2>
      {userRole ? (
        <div>
          <p>Welcome! Your role is: <strong>{userRole}</strong></p>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Dashboard;
