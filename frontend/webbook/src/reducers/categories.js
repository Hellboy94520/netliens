import { GET_CATEGORIES } from '../actions/types';

const initialState = {
  categories: null
};

export default function cat(state = initialState, action) {
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
