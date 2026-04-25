import React, { createContext, useEffect, useState } from 'react'
import { getMe, User } from './api'

export const AuthContext = createContext<{
	user: User | null
	login: (token: string) => void
	logout: () => void
	loading: boolean
} | null>(null)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
	const [user, setUser] = useState<User | null>(null)
	const [loading, setLoading] = useState(true)

	const fetchUser = async () => {
		try {
			const res = await getMe()
			setUser(res.data)
		} catch (e) {
			localStorage.removeItem('token')
			setUser(null)
		} finally {
			setLoading(false)
		}
	}

	const login = (token: string) => {
		localStorage.setItem('token', token)
		fetchUser()
	}

	const logout = () => {
		localStorage.removeItem('token')
		setUser(null)
	}

	useEffect(() => {
		if (localStorage.getItem('token')) {
			fetchUser()
		} else {
			setLoading(false)
		}
	}, [])

	return (
		<AuthContext.Provider value={{ user, login, logout, loading }}>
			{children}
		</AuthContext.Provider>
	)
}
