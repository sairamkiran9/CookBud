import useAuth from "./useAuth"
import { axiosPrivateInstance } from "../api/apiConfig"

export default function useLogout() {
    const { setUser, setAccessToken, setCSRFToken, setIsLoggedIn } = useAuth()

    const logout = async () => {
        try {
            await axiosPrivateInstance.post("auth/logout")

            setAccessToken(null)
            setCSRFToken(null)
            setUser({})
            setIsLoggedIn(false)

        } catch (error) {
            console.log(error)
        }
    }

    return logout
}