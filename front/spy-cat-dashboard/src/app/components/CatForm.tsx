import { useState } from "react";
import { CatCreate } from "./types";

export default function CatForm({ onCatCreated }: { onCatCreated: () => void }) {
  const [form, setForm] = useState<CatCreate>({
    name: "",
    years_of_experience: 0,
    breed: "Abyssinian",
    salary: 0,
  });
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8080/api/cats/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!response.ok) throw new Error("Failed to create cat");
      setForm({ name: "", years_of_experience: 0, breed: "Abyssinian", salary: 0 });
      setError(null);
      onCatCreated();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  };

  return (
    <div className="mb-4">
      <h2 className="text-xl mb-2">Add New Spy Cat</h2>
      {error && <div className="text-red-500 mb-2">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-2">
        <input
          type="text"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          placeholder="Name"
          className="border p-1 rounded"
          required
        />
        <input
          type="number"
          value={form.years_of_experience}
          onChange={(e) => setForm({ ...form, years_of_experience: parseInt(e.target.value) || 0 })}
          placeholder="Years of Experience"
          className="border p-1 rounded"
          required
        />
        <select
          value={form.breed}
          onChange={(e) => setForm({ ...form, breed: e.target.value as "Abyssinian" | "Bengal" | "Siamese" })}
          className="border p-1 rounded"
        >
          <option value="Abyssinian">Abyssinian</option>
          <option value="Bengal">Bengal</option>
          <option value="Siamese">Siamese</option>
        </select>
        <input
          type="number"
          value={form.salary}
          onChange={(e) => setForm({ ...form, salary: parseInt(e.target.value) || 0 })}
          placeholder="Salary"
          className="border p-1 rounded"
          required
        />
        <button type="submit" className="bg-green-500 text-white px-2 py-1 rounded">
          Add Cat
        </button>
      </form>
    </div>
  );
}