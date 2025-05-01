import { useState } from "react";
import axios from "axios";

interface Nutrient {
  name: string;
  amount: number;
  unit: string;
}

interface FoodItem {
  fdc_id: number;
  description: string;
  data_type: string;
  category: string;
  nutrients: Record<string, Nutrient>;
}

export default function App() {
  const [query, setQuery] = useState("");
  const [foods, setFoods] = useState<FoodItem[]>([]);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const searchFood = async () => {
    try {
      const response = await axios.get<FoodItem[]>(
        `http://localhost:8000/search_food?query=${query}`
      );
      setFoods(response.data);
      setExpandedId(null);
    } catch (error) {
      console.error("Error occured during API call", error);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex gap-2 mb-6">
        <input
          type="text"
          placeholder="Keresés (pl. banana)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") searchFood();
          }}
          className="flex-grow px-4 py-2 border rounded"
        />
        <button
          onClick={searchFood}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Keresés
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {foods.map((food) => (
          <div
            key={food.fdc_id}
            className="bg-white shadow-md rounded p-4 cursor-pointer hover:shadow-lg transition"
            onClick={() =>
              setExpandedId(expandedId === food.fdc_id ? null : food.fdc_id)
            }
          >
            <h2 className="text-xl font-semibold mb-1">{food.description}</h2>
            <p className="text-sm text-gray-500 mb-2">
              {food.category} ({food.data_type})
            </p>

            {expandedId === food.fdc_id && (
              <div className="mt-2 text-sm">
                <h3 className="font-semibold mb-1">Tápértékek:</h3>
                <ul className="list-disc list-inside space-y-1">
                  {Object.entries(food.nutrients).map(([key, value]) => (
                    <li key={key}>
                      {value.name}: {value.amount} {value.unit}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}