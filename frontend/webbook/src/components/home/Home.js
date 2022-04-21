import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { getCategories } from '../../actions/getCategories';

import { DataGrid, } from '@mui/x-data-grid';
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
          <Grid item xs={12}>
            <TextField id={'description'}
                label={'Description'}
                type={'description'}
                fullWidth/>
          </Grid>
        </Grid>
        <Grid container marginTop={'10px'}>
          <Grid item xs={12}>
            <Button variant="contained">Create</Button>
          </Grid>
        </Grid>
        <div style={{ width: '100%', height: '900px', marginTop: '10px'}}>
          { categories ? (
              <DataGrid
                marginTop={10}
                rows={categories}
                rowHeight={130}
                getRowId={(row) => row.id}
                columns={[
                  {
                    field: 'id',
                    headerName: 'id',
                    flex: 2,
                    align: 'center',
                    headerAlign: 'center',
                  },
                  {
                    field: 'name',
                    headerName: 'Name',
                    flex: 2,
                    align: 'center',
                    headerAlign: 'center',
                  },
                  {
                    field: 'description',
                    headerName: 'Description',
                    flex: 8,
                    align: 'left',
                    headerAlign: 'center',
                  }
                ]}
              />
            ) : (
              <h3>No Category</h3>
            )
          }
        </div>
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