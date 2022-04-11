import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { getCategories } from './actions/category';

import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { connect } from 'react-redux';


export class Home extends Component {

  static propTypes = {
    categories: PropTypes.array.isRequired,
    getCategories: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getCategories();
  }

  render() {
    return (
      <div className='category-form'>
        <Grid container>
          <Grid item xs={12}>
            <TextField id={'name'}
              label={'Name'}
              type={'name'}
              fullWidth/>
          </Grid>
        </Grid>
        <Grid container marginTop={'10px'}>
          <Grid item xs={12}>
            <Button variant="contained">Save</Button>
          </Grid>
        </Grid>
          {
            this.props.categories ? (
              <table className='category_list'>
              { this.props.categories.map((category) => (
              <tr key={category.id} className='category'>
                <td>{category.name}</td>
              </tr>
              ))}
              </table>
            ) : (
              <h3>No Category</h3>
            )
          }
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  categories: state.categories.categories
});

export default connect(
  mapStateToProps,
  { getCategories }
)(Home);