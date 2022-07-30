import useAxios from "../utils/useAxios"
import { GET_TEST } from "./types";

// GET LEADS
export const getTest = () => (dispatch, getState) => {
  const { axios } = useAxios()
  axios
    .get("/test/")
    .then((res) => {
      dispatch({
        type: GET_TEST,
        payload: res.data
      });
    })
    .catch(err => console.log(err));
};