import { useState } from "react";
import api from "../api/api";
export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const endpoint = isLogin ? "/login" : "/signup";

      const res = await api.post(endpoint, {
        email,
        password,
      });

      // LOGIN returns token
      if (isLogin) {
        localStorage.setItem("token", res.data.access_token);
        localStorage.setItem("user_email", res.data.user_email);
        alert("Login successful ✅");
        window.location.href = "/home"
      } else {
        alert("Signup successful ✅ Please login");
        setIsLogin(true);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div style={styles.container}>
      <form onSubmit={handleSubmit} style={styles.card}>
        <h2>{isLogin ? "Login" : "Signup"}</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={styles.input}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={styles.input}
        />

        {error && <p style={styles.error}>{error}</p>}

        <button type="submit" style={styles.button}>
          {isLogin ? "Login" : "Signup"}
        </button>

        <p style={styles.switch}>
          {isLogin ? "Don't have an account?" : "Already have an account?"}
          <span onClick={() => setIsLogin(!isLogin)} style={styles.link}>
            {isLogin ? " Signup" : " Login"}
          </span>
        </p>
      </form>
    </div>
  );
}

const styles: any = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  card: {
    width: "300px",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "8px",
  },
  input: {
    width: "100%",
    padding: "8px",
    marginBottom: "10px",
  },
  button: {
    width: "100%",
    padding: "8px",
    cursor: "pointer",
  },
  error: {
    color: "red",
    fontSize: "14px",
  },
  switch: {
    marginTop: "10px",
    fontSize: "14px",
  },
  link: {
    color: "blue",
    cursor: "pointer",
  },
};
