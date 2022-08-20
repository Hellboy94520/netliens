import { GET_CATEGORIES } from '../actions/types';

const initialState = {
  categories_list: ["toot", "tiit"]
};

export default function cat(state = initialState, action) {
  console.log("reducers/Categories: ")
  console.log(action)
  // return {
  //   // Return everything defined in initialState
  //   ...state,
  //   categories_list: action.payload
  // };

  switch(action.type) {
    case GET_CATEGORIES:
      console.log("Action=GET_CATEGORIES: "+action.payload)
      return {
        // Return everything defined in initialState
        ...state,
        categories_list: action.payload
      };
    default:
      return state;
  }
}
