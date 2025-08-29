import React, { useEffect, useState } from "react";
import { getRecipes } from "../api";

function RecipeList() {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    async function fetchRecipes() {
      const res = await getRecipes();
      setRecipes(res);
    }
    fetchRecipes();
  }, []);

  return (
    <div>
      <h2>Recipes</h2>
      {recipes.map(r => (
        <div key={r.id}>
          <h3>{r.title}</h3>
          <p>{r.instructions}</p>
          <small>By {r.user.username}</small>
        </div>
      ))}
    </div>
  );
}

export default RecipeList;
