import { GET_TEST } from '../actions/types';

const initialState = {
  test: null
};

export default function cat(state = initialState, action) {
  switch(action.type) {
    case GET_TEST:
      return {
        // Return everything defined in initialState
        ...state,
        test: action.payload
      };
    default:
      return state;
  }
}
