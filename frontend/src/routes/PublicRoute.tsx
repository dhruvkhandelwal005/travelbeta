import { Navigate } from "react-router-dom"
import type { ReactNode } from "react"
import { isAuthenticated } from "../components/auth"

const PublicRoute = ({ children }: { children: ReactNode }) => {
  if (isAuthenticated()) {
    return <Navigate to="/home" replace />
  }
  return <>{children}</>
}

export default PublicRoute
