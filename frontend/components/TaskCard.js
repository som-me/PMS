export default function TaskCard({ task }) {
    return (
        <div className="bg-white p-4 rounded-xl shadow hover:shadow-lg transition">
            <h2 className="text-lg font-semibold text-gray-800">{task.title}</h2>
            <p className="text-sm text-gray-600 mt-2">{task.description}</p>
            <div className="mt-3 flex justify-between items-center">
                <span
                    className={`text-sm px-3 py-1 rounded-full ${
                        task.status === "Completed"
                            ? "bg-green-100 text-green-700"
                            : "bg-yellow-100 text-yellow-700"
                    }`}
                >
                    {task.status}
                </span>
                <p className="text-xs text-gray-500">
                    Due: {task.due_date || "—"}
                </p>
            </div>
        </div>
    );
}
