import { Routes, Route } from "react-router-dom"
import Auth from "./pages/Auth"
import Home from "./pages/home"
import ProtectedRoute from "./routes/ProtectedRoute"
import PublicRoute from "./routes/PublicRoute"
import AuthRedirect from "./components/AuthRedirect"

function App() {
  return (
    <Routes>
      {/* Root decides based on token */}
      <Route path="/" element={<AuthRedirect />} />

      {/* Login / Signup page */}
      <Route
        path="/auth"
        element={
          <PublicRoute>
            <Auth />
          </PublicRoute>
        }
      />

      {/* Home (Protected) */}
      <Route
        path="/home"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

export default App
