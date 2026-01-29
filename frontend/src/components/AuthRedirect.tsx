import { Navigate } from "react-router-dom"
import { isAuthenticated } from "./auth"

const AuthRedirect = () => {
  return isAuthenticated()
    ? <Navigate to="/home" replace />
    : <Navigate to="/auth" replace />
}

export default AuthRedirect
