import axios from 'axios';

import { GET_CATEGORIES } from './types';

// GET LEADS
export const getCategories = () => dispatch => {
  axios.get('/category/').then(res => {
    dispatch({
      type: GET_CATEGORIES,
      payload: res.data
    });
  }).catch(err => console.log("ALEX"+err))
}