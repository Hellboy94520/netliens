import axios from "axios";

import { GET_CATEGORIES } from "./types";

// GET LEADS
export const getCategories = () => (dispatch, getState) => {
  console.log("actions/getCategories")
  dispatch({
    type: GET_CATEGORIES,
    payload: [ 'baak1', 'baak2' ]
  });
  // axios
  //   .get("/category/list/")
  //   .then((res) => {
  //     dispatch({
  //       type: GET_CATEGORIES,
  //       payload: res.data
  //     });
  //   })
  //   .catch(err => console.log(err));
};