import { useState } from "react";
import { Cat } from "./types";

export default function EditCatModal({
  cat,
  onClose,
  onUpdate,
}: {
  cat: Cat;
  onClose: () => void;
  onUpdate: () => void;
}) {
  const [salary, setSalary] = useState(cat.salary);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8080/api/cats/${cat.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ salary }),
      });
      if (!response.ok) throw new Error("Failed to update cat");
      onUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-4 rounded shadow-lg">
        <h2 className="text-xl mb-2">Edit Salary for {cat.name}</h2>
        {error && <div className="text-red-500 mb-2">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-2">
          <input
            type="number"
            value={salary}
            onChange={(e) => setSalary(parseInt(e.target.value) || 0)}
            className="border p-1 rounded w-full"
            required
          />
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="bg-gray-500 text-white px-2 py-1 rounded"
            >
              Cancel
            </button>
            <button type="submit" className="bg-blue-500 text-white px-2 py-1 rounded">
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}