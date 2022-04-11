import { GET_CATEGORIES } from '../actions/types.js';

const initialState = {
  categories: []
};

export default function getCategories(state = initialState, action) {
  switch(action.type) {
    case GET_CATEGORIES:
      return {
        // Return everything defined in initialState
        ...state,
        categories: action.payload
      };
    default:
      return state;
  }
}
