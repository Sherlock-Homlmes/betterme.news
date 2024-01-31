const fetchWithAuth = async (url: string, options?: any) => {
  const token = window.localStorage.getItem('Authorization');
  console.log(token)
  if(!token){
    console.log("No token")
  }
  return fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    ...options,
  });
};

export default fetchWithAuth;
