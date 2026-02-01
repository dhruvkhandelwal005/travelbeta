import { Navigate } from "react-router-dom"
import type { ReactNode } from "react"
import { isAuthenticated } from "../components/api"

const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/auth" replace />
  }
  return <>{children}</>
}

export default ProtectedRoute
