export const getToken = () => {
  return localStorage.getItem("token")
}

export const isAuthenticated = () => {
  return !!localStorage.getItem("token")
}

export const logout = () => {
  localStorage.removeItem("token")
  localStorage.removeItem("user_email")
  window.location.href = "/auth"
}
