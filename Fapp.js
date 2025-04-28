import { useState } from "react";
import axios from "axios";

function App() {
  const [foods, setFoods] = useState([]);

  const searchFood = async () => {
    const response = await axios.get("http://localhost:8000/search_food?query=banana");
    setFoods(response.data);
  };

  return (
    <div>
      <button onClick={searchFood}>Keresés</button>
      <ul>
        {foods.map((food, index) => (
          <li key={index}>{food.description}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;