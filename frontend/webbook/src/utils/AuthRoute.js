import { Route, Navigate, useNavigate, useLocation } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../content/AuthContext";

const AuthRoute = ({ children }) => {
  let { user } = useContext(AuthContext);
  let location = useLocation();
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children
};
export default AuthRoute;