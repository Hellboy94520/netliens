import { useEffect, useState } from "react";
import { connect } from 'react-redux'
import { getCategories } from "../../actions/getCategories";
import categories from "../../reducers/categories";


const CategoryPage = (props) => {
  // const api = useAxios();

  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await api.get("/category/list/");
  //       setRes(response.data);
  //     } catch {
  //       setRes("Something went wrong");
  //     }
  //   };
  //   fetchData();
  //   // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, []);

  const [categories, setCategories] = useState(null)


  useEffect(() => {
    setCategories(props.getCategories().payload)
    console.log(categories)
  }, [])

  return (
    <div>
      <h1>Categories</h1>
      { categories ? categories : "Vide" }
      {/* { categories.map((content, index) => content) } */}
      {/* { props.categories ? "OK" : "NOK"} */}
      {/* {props.categories ? (
          props.categories.map((c, _) => (
            <p>{c.id} {c.name}</p>
          ))
        ) : (
          "Aucune Catégorie"
        )
      } */}
    </div>
  );
}
const mapStateToProps = (state) => {
  console.log("CategoryPage-mapStateToProps")
  return { categories: state.categories };
};

const mapDispatchToProps = dispatch => {
  console.log("CategoryPage-mapDispatchToProps")
	return {
		getCategories: () => dispatch(getCategories())
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(CategoryPage);
