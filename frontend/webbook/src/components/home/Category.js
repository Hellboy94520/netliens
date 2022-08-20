
import { useEffect, useState } from "react";
import useAxios from "../../utils/useAxios";

function CategoryPage() {
  const [res, setRes] = useState("");
  const api = useAxios();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/category/list/");
        setRes(response.data);
      } catch {
        setRes("Something went wrong");
      }
    };
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      <h1>Categories</h1>
      {res ? (
          res.map((c, _) => (
            <p>{c.id} {c.name}</p>
          ))
        ) : (
          "Aucune Catégorie"
        )
      }
    </div>
  );
}

export default CategoryPage;