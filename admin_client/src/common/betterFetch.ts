const fetchWithAuth = async (url: string, options?: any) => {
  const token = window.localStorage.getItem("Authorization");
  return fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    ...options,
  });
};

export default fetchWithAuth;
