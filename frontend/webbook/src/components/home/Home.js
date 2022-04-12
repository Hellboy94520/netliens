import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { getCategories } from '../../actions/category';

import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { connect } from 'react-redux';


export class Home extends Component {

  static propTypes = {
    getCategories: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getCategories()
  }

  render() {
    const { categories } = this.props;
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
        { console.log(categories) }
          {
            categories ? (
              <table className='category_list'>
              { categories.map((category) => (
              <tr key={category.id} className='category'>
                <td>{category.name}: {category.description}</td>
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