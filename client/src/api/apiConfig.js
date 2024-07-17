import axios from "axios"

const API_URL = process.env.REACT_APP_API_URL;
// "http://ec2-54-227-245-173.compute-1.amazonaws.com:8000/" // "http://127.0.0.1:8000/"

export const axiosInstance = axios.create({
    baseURL: API_URL,
    withCredentials: true,
    headers: {
        "Content-Type": "application/json"
    }
})

export const axiosPrivateInstance = axios.create({
    baseURL: API_URL,
    withCredentials: true,
    headers: {
        "Content-Type": "application/json"
    }
})