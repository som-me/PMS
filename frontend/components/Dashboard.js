'use client';
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ProjectCard from "@/components/ProjectCard";
import CreateProjectModal from "@/components/CreateProjectModal";

export default function Dashboard() {
    const router = useRouter();
    const [projects, setProjects] = useState([]);
    const [error, setError] = useState("");
    const [showModal, setShowModal] = useState(false);
    const BACKEND_URL = "http://127.0.0.1:8000";
    const [token, setToken] = useState("");

    const fetchProjects = async () => {
        const storedToken = localStorage.getItem("token");
        if (!storedToken) {
            router.push("/");
            return;
        }
        setToken(storedToken);

        try {
            const res = await fetch(`${BACKEND_URL}/api/projects`, {
                headers: { Authorization: `Bearer ${storedToken}` },
            });

            if (res.status === 401) throw new Error("Unauthorized");
            if (res.status === 404) throw new Error("Projects endpoint not found");
            if (!res.ok) throw new Error("Server Error");

            const data = await res.json();
            setProjects(data);
        } catch (err) {
            setError(err.message);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        router.push("/");
    };

    useEffect(() => {
        fetchProjects();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <div className="min-h-screen bg-gray-100 relative p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-blue-700">Dashboard</h1>
                <div className="flex items-center gap-3">
                    <button
                        onClick={handleLogout}
                        className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
                    >
                        Logout
                    </button>
                </div>
            </div>

            {error && <p className="text-red-600 mb-4">{error}</p>}

            {projects.length === 0 ? (
                <p className="text-gray-600 text-lg">No projects yet. Create one!</p>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                    {projects.map((proj) => (
                        <ProjectCard key={proj.id} project={proj} token={token} onProjectUpdated={fetchProjects} />
                    ))}
                </div>
            )}

            {/* Floating New Project Button */}
            <button
                onClick={() => setShowModal(true)}
                className="fixed bottom-8 right-8 bg-blue-600 text-white px-5 py-3 rounded-full shadow-lg hover:bg-blue-700 transition transform hover:scale-105"
            >
                + New Project
            </button>

            {/* Create Project Modal */}
            {showModal && (
                <CreateProjectModal
                    onClose={() => setShowModal(false)}
                    onCreated={fetchProjects}
                />
            )}
        </div>
    );
}
