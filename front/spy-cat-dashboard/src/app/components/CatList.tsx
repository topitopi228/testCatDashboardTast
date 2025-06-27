import { Cat } from "./types";

interface CatListProps {
  cats: Cat[];
  onEdit: (cat: Cat) => void;
  onDelete: (catId: number) => void;
}

export default function CatList({ cats, onEdit, onDelete }: CatListProps) {
  const handleDelete = async (catId: number) => {
    if (confirm("Are you sure you want to delete this cat?")) {
      try {
        const response = await fetch(`http://localhost:8080/api/cats/${catId}`, {
          method: "DELETE",
        });
        if (!response.ok) throw new Error("Failed to delete cat");
        onDelete(catId);
      } catch (err) {
        alert(err instanceof Error ? err.message : "Unknown error");
      }
    }
  };

  return (
    <div className="mt-4">
      <h2 className="text-xl mb-2">Spy Cats</h2>
      <ul className="space-y-2">
        {cats.map((cat) => (
          <li key={cat.id} className="border p-2 flex justify-between">
            <span>
              {cat.name} (Salary: ${cat.salary}, Experience: {cat.years_of_experience} yrs, Breed: {cat.breed})
            </span>
            <div>
              <button
                onClick={() => onEdit(cat)}
                className="bg-blue-500 text-white px-2 py-1 mr-2 rounded"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(cat.id)}
                className="bg-red-500 text-white px-2 py-1 rounded"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}