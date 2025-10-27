'use client';
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function AuthForm() {
    const router = useRouter();
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        password: "",
        role: "developer",
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const BACKEND_URL = "https://pms-backend-cmdn.onrender.com";


    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const testConnection = async () => {
        try {
            const res = await fetch(`${BACKEND_URL}/api/auth/test`);
            const data = await res.json();
            console.log("Backend connection successful:", data);
            alert("✅ Backend Connected!");
        } catch (err) {
            console.error("Backend connection failed:", err);
            alert("❌ Backend Connection Failed!");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const endpoint = isLogin
                ? `${BACKEND_URL}/api/auth/login`
                : `${BACKEND_URL}/api/auth/register`;

            const res = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            let data;
            try {
                data = await res.json();
            } catch {
                throw new Error("Unexpected response (not JSON)");
            }

            if (!res.ok) {
                let message = "Something went wrong";
                if (data?.detail) {
                    if (Array.isArray(data.detail)) {
                        message = data.detail.map(d => d.msg || JSON.stringify(d)).join(", ");
                    } else if (typeof data.detail === "object") {
                        message = data.detail.msg || JSON.stringify(data.detail);
                    } else {
                        message = data.detail;
                    }
                }
                throw new Error(message);
            }

            if (isLogin) {
                localStorage.setItem("token", data.access_token);
                localStorage.setItem("role", data.role || "user");
                router.push("/dashboard");
            } else {
                alert("✅ Registration successful! You can now log in.");
                setIsLogin(true);
            }
        } catch (err) {
            console.error("Auth error:", err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 w-full sm:max-w-lg md:max-w-xl flex items-center justify-center px-4 sm:px-6 lg:px-8">
            <div className="bg-white p-10 rounded-2xl shadow-lg w-full sm:max-w-lg md:max-w-xl lg:max-w-2xl transition-all duration-300">
                <h2 className="text-3xl text-blue-600 font-bold mb-8 text-center">
                    {isLogin ? "Login" : "Register"}
                </h2>

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label className="block text-gray-700 text-lg">Name</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            required
                            className="w-full border text-gray-500 border-gray-300 rounded-lg p-3 mt-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    <div>
                        <label className="block text-gray-700 text-lg">Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            className="w-full border text-gray-500 border-gray-300 rounded-lg p-3 mt-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    <div>
                        <label className="block text-gray-700 text-lg">Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            className="w-full border text-gray-500 border-gray-300 rounded-lg p-3 mt-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    {!isLogin && (
                        <div>
                            <label className="block text-gray-700 text-lg">Role</label>
                            <select
                                name="role"
                                value={formData.role}
                                onChange={handleChange}
                                className="w-full border text-gray-500 border-gray-300 rounded-lg p-3 mt-1"
                            >
                                <option value="admin" className="text-gray-500">Admin</option>
                                <option value="manager" className="text-gray-500">Project Manager</option>
                                <option value="developer" className="text-gray-500">Developer</option>
                            </select>
                        </div>
                    )}

                    {error && (
                        <p className="text-red-500 text-center text-sm">{error}</p>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition text-lg"
                    >
                        {loading ? "Please wait..." : isLogin ? "Login" : "Register"}
                    </button>
                </form>

                <div className="text-center mt-5">
                    <button
                        onClick={() => setIsLogin(!isLogin)}
                        className="text-blue-600 hover:underline text-lg"
                    >
                        {isLogin ? "Create an account" : "Already have an account? Login"}
                    </button>
                </div>

                <button
                    type="button"
                    onClick={testConnection}
                    className="w-full bg-green-600 text-white p-3 rounded-lg hover:bg-green-700 transition mt-3 text-lg"
                >
                    Test Connection
                </button>
            </div>
        </div>
    );
}
