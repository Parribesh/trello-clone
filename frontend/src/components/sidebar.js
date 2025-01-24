import React from "react";
import { useNavigate } from "react-router-dom"; // Updated from `useHistory` to `useNavigate`
import { List, ListItem, ListItemText, Divider } from "@mui/material";
import dashboardMenus from "../data/dashboardMenus.json";
import axiosInstance from "../config/axiosConfig";

const Sidebar = () => {
  const navigate = useNavigate();

  const handleMenuClick = async (route) => {
    if (route === "/logout") {
      // Handle logout logic here (e.g., clear tokens, call API)
      console.log("Logging out...");
      try {
        // Make a request to the logout endpoint
        await axiosInstance.post("/auth/logout", {}, { withCredentials: true });

        // Navigate to the login page
        navigate("/login");
      } catch (error) {
        console.error("Logout failed:", error);
        // Optionally handle errors (e.g., show a message to the user)
      }
    } else {
      navigate(route);
    }
  };

  return (
    <div className="sidebar">
      <List>
        {dashboardMenus.map((menu, index) => (
          <React.Fragment key={index}>
            <ListItem button onClick={() => handleMenuClick(menu.route)}>
              <ListItemText primary={menu.label} />
            </ListItem>
            {index < dashboardMenus.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </List>
    </div>
  );
};

export default Sidebar;
