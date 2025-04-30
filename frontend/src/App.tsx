import React, { useState } from "react";
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
  nutrients: { [key: string]: Nutrient };
}

function App() {
  const [foods, setFoods] = useState<FoodItem[]>([]);

  const searchFood = async () => {
    try {
      const response = await axios.get<FoodItem[]>("http://localhost:8000/search_food?query=banana");
      setFoods(response.data);
    } catch (error) {
      console.error("Error occured during API call", error);
    }
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <button
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded"
        onClick={searchFood}
      >
        Keresés
      </button>

      <div className="mt-6 space-y-6">
        {foods.map((food) => (
          <div key={food.fdc_id} className="p-4 border rounded shadow-md bg-white">
            <h2 className="text-xl font-bold mb-1">{food.description}</h2>
            <p className="text-gray-600 mb-2">{food.category} ({food.data_type})</p>

            <table className="table-auto w-full text-sm border">
              <thead>
                <tr className="bg-gray-200">
                  <th className="border px-2 py-1">Tápanyag</th>
                  <th className="border px-2 py-1">Mennyiség</th>
                  <th className="border px-2 py-1">Egység</th>
                </tr>
              </thead>
              <tbody>
                {Object.values(food.nutrients).map((nutrient, i) => (
                  <tr key={i}>
                    <td className="border px-2 py-1">{nutrient.name}</td>
                    <td className="border px-2 py-1">{nutrient.amount}</td>
                    <td className="border px-2 py-1">{nutrient.unit}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;