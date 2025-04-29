import { useState } from "react";
import axios from "axios";

interface FoodItem{
  description: string;
}

function App() {
  const [foods, setFoods] = useState([]);

  const searchFood = async () => {
    try{
      const response = await axios.get<FoodItem>("http://localhost:8000/search_food?query=banana");
      setFoods(response.data);
    } catch (error){
      console.error("Error occured during API call", error);
    }
  };

  return (
    <div className="p-4">
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={searchFood}
      >
        Keresés
      </button>
      <ul className="mt-4 list-disc list-inside">
        {foods.map((food, index) => (
          <li key={index}>{food.description}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
