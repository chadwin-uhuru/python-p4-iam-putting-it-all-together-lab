const BASE_URL = "http://127.0.0.1:5555";

export async function signup(userData) {
  const res = await fetch(`${BASE_URL}/signup`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(userData),
    credentials: "include"
  });
  return res.json();
}

export async function login(userData) {
  const res = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(userData),
    credentials: "include"
  });
  return res.json();
}

export async function checkSession() {
  const res = await fetch(`${BASE_URL}/check_session`, {
    credentials: "include"
  });
  return res.json();
}

export async function logout() {
  const res = await fetch(`${BASE_URL}/logout`, {
    method: "DELETE",
    credentials: "include"
  });
  return res.json();
}

export async function getRecipes() {
  const res = await fetch(`${BASE_URL}/recipes`, {
    credentials: "include"
  });
  return res.json();
}

export async function createRecipe(recipeData) {
  const res = await fetch(`${BASE_URL}/recipes`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(recipeData),
    credentials: "include"
  });
  return res.json();
}
