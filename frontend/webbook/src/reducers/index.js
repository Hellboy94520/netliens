import { combineReducers } from "redux";
import test from './test'
import categories from "./categories";

// Cf src/common/routeReducer
export default combineReducers({
  // test: test,
  categories: categories,
});
