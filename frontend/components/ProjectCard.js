// frontend/components/ProjectCard.js
'use client';
import { useState, useEffect } from "react";
import TaskCard from "./TaskCard";
import CreateTaskModal from "./CreateTaskModal";

export default function ProjectCard({ project, token, onProjectUpdated }) {
    const [tasks, setTasks] = useState([]);
    const [showTaskModal, setShowTaskModal] = useState(false);
    const [editingTask, setEditingTask] = useState(null);
    const BACKEND_URL = "http://127.0.0.1:8000";

    const fetchTasks = async () => {
        if (!token) return;
        try {
            const res = await fetch(`${BACKEND_URL}/api/projects/${project.id}/tasks`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (!res.ok) {
                console.error("Failed to load tasks for project", project.id, res.status);
                setTasks([]);
                return;
            }
            const data = await res.json();
            setTasks(data);
        } catch (err) {
            console.error("Error fetching tasks:", err);
            setTasks([]);
        }
    };

    useEffect(() => {
        fetchTasks();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const openAddModal = () => {
        setEditingTask(null);
        setShowTaskModal(true);
    };

    const openEditModal = (task) => {
        setEditingTask(task);
        setShowTaskModal(true);
    };

    const handleCreatedOrUpdated = () => {
        // refresh tasks and notify parent (dashboard) if needed
        fetchTasks();
        if (typeof onProjectUpdated === "function") onProjectUpdated();
        setShowTaskModal(false);
        setEditingTask(null);
    };

    return (
        <div className="bg-white rounded-xl shadow-md p-4 hover:shadow-lg transition relative">
            <h2 className="text-xl font-semibold text-blue-700 mb-2">{project.name}</h2>
            <p className="text-gray-600 mb-2">{project.description || "No description"}</p>
            <p className="text-sm text-gray-500 mb-4">
                Status: <span className="font-medium">{project.status || "Pending"}</span>
            </p>

            {/* Add / Edit Task Buttons */}
            <div className="flex gap-2 items-center">
                {tasks.length === 0 ? (
                    <button
                        onClick={openAddModal}
                        className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
                    >
                        + Add Task
                    </button>
                ) : (
                    <button
                        onClick={() => openEditModal(tasks[0])}
                        className="bg-yellow-600 text-white px-3 py-1 rounded hover:bg-yellow-700 transition"
                    >
                        Edit Task
                    </button>
                )}
                <button
                    onClick={fetchTasks}
                    className="bg-gray-200 text-gray-800 px-3 py-1 rounded hover:bg-gray-300 transition"
                >
                    Refresh
                </button>
            </div>

            {/* Show tasks under project card */}
            {tasks.length > 0 && (
                <div className="mt-4 space-y-3">
                    {tasks.map((t) => (
                        <TaskCard key={t.id} task={t} onEdit={() => openEditModal(t)} />
                    ))}
                </div>
            )}

            {/* Task Modal (create or edit) */}
            {showTaskModal && (
                <CreateTaskModal
                    projectId={project.id}
                    token={token}
                    existingTask={editingTask}
                    onClose={() => { setShowTaskModal(false); setEditingTask(null); }}
                    onCreated={handleCreatedOrUpdated}
                />
            )}
        </div>
    );
}
