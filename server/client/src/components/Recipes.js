import React, { useEffect, useState } from "react";
import axios from "axios";

function Recipes() {
  const [recipes, setRecipes] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    axios.get("/recipes", { withCredentials: true })
      .then(res => setRecipes(res.data))
      .catch(() => setError("You must be logged in to view recipes."));
  }, []);

  return (
    <div>
      <h2>All Recipes</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {recipes.map(recipe => (
          <li key={recipe.id}>
            <h3>{recipe.title}</h3>
            <p>{recipe.instructions}</p>
            <p>Time to complete: {recipe.minutes_to_complete} mins</p>
            <p>Author: {recipe.user.username}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Recipes;
