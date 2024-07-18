import axios from "axios"

const API_URL = process.env.REACT_APP_API_URL;
// "http://ec2-54-227-245-173.compute-1.amazonaws.com:8000/" // "http://127.0.0.1:8000/"
export const CSRF_COOKIE_NAME = 'csrftoken'; // CSRF cookie name
export const CSRF_HEADER_NAME = 'X-CSRFToken'; // CSRF header name

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

export const axiosFetchRecommendations = async (ingredients, spiceLevel, cuisineType, accessToken, csrftoken) => {
    try {
        const response = await axios.post(
            `${API_URL}auth/recommendation/`,
            {
                ingredients,
                spice_level: spiceLevel,
                cuisine_type: cuisineType
            },
            {
                headers: {
                    "Authorization": "Bearer " + accessToken,
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                },
                xsrfCookieName: CSRF_COOKIE_NAME,
                xsrfHeaderName: CSRF_HEADER_NAME
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        throw error;
    }
};