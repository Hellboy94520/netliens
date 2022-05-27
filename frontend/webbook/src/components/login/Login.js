import React, { Component } from "react";
import axiosInstance from "../../axiosApi";

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {email: "", password: ""};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleSubmitWThen = this.handleSubmitWThen.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    handleSubmitWThen(event){
        event.preventDefault();
        console.log("POSTING ! "+ this.state.email + " " + this.state.password)
        axiosInstance.post('/token/', {
                email: this.state.email,
                password: this.state.password
            }).then(
                result => {
                    axiosInstance.defaults.headers['Authorization'] = "JWT " + result.data.access;
                    localStorage.setItem('access_token', result.data.access);
                    localStorage.setItem('refresh_token', result.data.refresh);
                }
            ).catch (error => {
                throw error;
            })
    }

    async handleSubmit(event) {
        event.preventDefault();
        try {
            const response = await axiosInstance.post('/token/', {
                email: this.state.email,
                password: this.state.password
            });
            axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            console.log("Authentification réussi !")
            return response;
        } catch (error) {
            throw error;
        }
    }

    render() {
        return (
            <div>
                Login
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Email:
                        <input name="email" type="text" value={this.state.email} onChange={this.handleChange}/>
                    </label>
                    <label>
                        Password:
                        <input name="password" type="password" value={this.state.password} onChange={this.handleChange}/>
                    </label>
                    <input type="submit" value="Submit"/>
                </form>
            </div>
        )
    }
}
export default Login;