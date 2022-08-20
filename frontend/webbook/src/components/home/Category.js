import { useEffect, useState } from "react";
import { connect } from 'react-redux'
import { getCategories } from "../../actions/getCategories";
import categories from "../../reducers/categories";


const CategoryPage = (props) => {
  const [ categories ] = useState(null)

  useEffect(() => {
    console.log("useEffect")
    // console.log(props.getCategories())
    // // setCategories(props.getCategories().categories.categories_list)
    console.log(props.categories)
  }, [])

  return (
    <div>
      <h1>Categories</h1>
      { props.categories ? props.categories : "Vide" }
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
  const { categories } = state
  return { categories: categories.categories_list };
};

const mapDispatchToProps = dispatch => {
  console.log("CategoryPage-mapDispatchToProps")
	return {
		getCategories: () => dispatch(getCategories())
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(CategoryPage);
