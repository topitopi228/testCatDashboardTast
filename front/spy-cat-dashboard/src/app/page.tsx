"use client";
import { useState, useEffect } from "react";
import CatList from "./components/CatList";
import CatForm from "./components/CatForm";
import EditCatModal from "./components/EditCatModal";
import { Cat } from "./components/types";

export default function Home() {
  const [cats, setCats] = useState<Cat[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [selectedCat, setSelectedCat] = useState<Cat | null>(null);

  const fetchCats = async () => {
    try {
      const response = await fetch("http://localhost:8080/api/cats/");
      if (!response.ok) throw new Error("Failed to fetch cats");
      const data = await response.json();
      setCats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  };

  useEffect(() => {
     fetchCats();

  }, []);

  const handleCatCreated = () => {
    fetchCats();
  };

  const handleCatUpdated = () => {
    setSelectedCat(null);
    fetchCats();
  };

  const handleCatDeleted = (catId: number) => {
    setCats(cats.filter((cat) => cat.id !== catId));
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Spy Cats Management Dashboard</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <CatForm onCatCreated={handleCatCreated} />
      <CatList
        cats={cats}
        onEdit={(cat) => setSelectedCat(cat)}
        onDelete={handleCatDeleted}
      />
      {selectedCat && (
        <EditCatModal
          cat={selectedCat}
          onClose={() => setSelectedCat(null)}
          onUpdate={handleCatUpdated}
        />
      )}
    </div>
  );
}

